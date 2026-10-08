from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from backend.spotify_client import get_spotify_token, search_track
from backend.lastfm_client import get_similar_tracks
from backend.database import create_db_and_tables, get_session
from backend.models import Track
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa quando a API ligar
    create_db_and_tables()
    yield
    # Executa quando a API desligar

app = FastAPI(title="Songseeker MVP", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Songseeker API"}

@app.get("/api/token-status")
async def check_token():
    token = await get_spotify_token()
    if token:
        return {"status": "ok", "token_preview": f"{token[:10]}..."}
    return {"status": "error", "message": "Failed to retrieve token. Verifique o arquivo .env"}

@app.get("/api/search")
async def search_and_cache(q: str, session: Session = Depends(get_session)):
    # 1. Faz a busca no Spotify
    spotify_track = await search_track(q)
    if not spotify_track:
        raise HTTPException(status_code=404, detail="Música não encontrada no Spotify")
        
    spotify_id = spotify_track.get("id")
    
    # 2. Verifica se a música já existe no nosso banco de dados
    statement = select(Track).where(Track.spotify_id == spotify_id)
    db_track = session.exec(statement).first()
    
    if db_track:
        # Se já existe, retorna os dados do nosso cache (SQLite)
        return {"source": "cache_sqlite", "track": db_track}
        
    # Extrai a URL da capa do álbum
    album_images = spotify_track.get("album", {}).get("images", [])
    image_url = album_images[0]["url"] if album_images else None
    
    # 4. Salva no banco de dados
    new_track = Track(
        spotify_id=spotify_id,
        name=spotify_track.get("name"),
        artist_name=spotify_track["artists"][0]["name"] if spotify_track.get("artists") else "Desconhecido",
        album_image_url=image_url,
        preview_url=spotify_track.get("preview_url")
    )
    
    session.add(new_track)
    session.commit()
    session.refresh(new_track)
    
    return {"source": "spotify_api", "track": new_track}

@app.get("/api/recommendations")
async def get_recommendations(artist: str, track: str):
    # 1. Pega as similares no Last.fm
    similar_data = await get_similar_tracks(artist, track, limit=5)
    
    if not similar_data:
        return {"recommendations": []}
        
    # 2. Busca os detalhes no Spotify para pegar Capa e ID para o Iframe
    async def fetch_spotify_details(t):
        query = f"track:{t['name']} artist:{t['artist']}"
        spotify_info = await search_track(query)
        if spotify_info:
            album_images = spotify_info.get("album", {}).get("images", [])
            image_url = album_images[0]["url"] if album_images else None
            return {
                "name": spotify_info.get("name"),
                "artist": spotify_info["artists"][0]["name"] if spotify_info.get("artists") else t["artist"],
                "spotify_id": spotify_info.get("id"),
                "album_image_url": image_url
            }
        return None

    # Roda as buscas no Spotify em paralelo para ser rápido
    tasks = [fetch_spotify_details(t) for t in similar_data]
    results = await asyncio.gather(*tasks)
    
    # Filtra as que não achou no Spotify
    final_recs = [r for r in results if r is not None]
    
    return {"recommendations": final_recs}
