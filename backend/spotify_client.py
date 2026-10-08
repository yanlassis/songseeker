import os
import base64
import httpx
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

_cached_token = None

async def get_spotify_token():
    global _cached_token
    # Para o MVP, estamos armazenando no estado global, mas idealmente 
    # devemos checar o tempo de expiração (expires_in ~3600s).
    if _cached_token:
        return _cached_token
        
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("Spotify credentials missing no arquivo .env")
        return None

    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            _cached_token = token_data.get("access_token")
            return _cached_token
        else:
            print(f"Error fetching token: {response.text}")
            return None

async def search_track(query: str):
    token = await get_spotify_token()
    if not token:
        return None
        
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get("tracks", {}).get("items", [])
            if tracks:
                return tracks[0]
        return None

async def get_audio_features(spotify_id: str):
    token = await get_spotify_token()
    if not token:
        return None
        
    url = f"https://api.spotify.com/v1/audio-features/{spotify_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
