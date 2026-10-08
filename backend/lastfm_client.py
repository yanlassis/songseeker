import os
import httpx
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

async def get_similar_tracks(artist_name: str, track_name: str, limit: int = 5):
    if not LASTFM_API_KEY:
        print("LASTFM_API_KEY missing no arquivo .env")
        return []
        
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getsimilar",
        "artist": artist_name,
        "track": track_name,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            similar_tracks = data.get("similartracks", {}).get("track", [])
            
            # Formatando o retorno
            results = []
            for t in similar_tracks:
                results.append({
                    "name": t.get("name"),
                    "artist": t.get("artist", {}).get("name")
                })
            return results
        else:
            print(f"Error fetching from Last.fm: {response.text}")
            return []
