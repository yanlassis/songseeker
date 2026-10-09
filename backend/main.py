from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from backend.spotify_client import get_spotify_token, search_track
from backend.lastfm_client import get_similar_tracks
from backend.database import create_db_and_tables, get_session
from backend.models import Track
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Songseeker MVP", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/api/token-status")
async def check_token():
    token = await get_spotify_token()
    if token:
        return {"status": "ok"}
    return JSONResponse(
        status_code=503,
        content={"status": "error", "message": "Failed to retrieve token. Verifique o arquivo .env"},
    )

@app.get("/api/search")
async def search_and_cache(q: str, session: Session = Depends(get_session)):

    spotify_track = await search_track(q)
    if not spotify_track:
        raise HTTPException(status_code=404, detail="Música não encontrada no Spotify")

    spotify_id = spotify_track.get("id")

    statement = select(Track).where(Track.spotify_id == spotify_id)
    db_track = session.exec(statement).first()

    if db_track:
        return {"source": "cache_sqlite", "track": db_track}

    album_images = spotify_track.get("album", {}).get("images", [])
    image_url = album_images[0]["url"] if album_images else None

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

    similar_data = await get_similar_tracks(artist, track, limit=8)

    if not similar_data:
        return {"recommendations": []}

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

    tasks = [fetch_spotify_details(t) for t in similar_data]
    results = await asyncio.gather(*tasks)

    final_recs = [r for r in results if r is not None]

    return {"recommendations": final_recs}
