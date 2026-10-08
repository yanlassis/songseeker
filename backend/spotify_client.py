import os
import time
import base64
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# O token do Spotify expira em ~3600s. Renovamos um pouco antes
# para não usar um token que vence no meio de uma requisição.
TOKEN_REFRESH_MARGIN = 60

_cached_token = None
_expires_at = 0.0
_token_lock = None

def invalidate_token():
    # Chamar quando a API responder 401, para forçar um token novo.
    global _cached_token, _expires_at
    _cached_token = None
    _expires_at = 0.0

async def get_spotify_token():
    global _cached_token, _expires_at, _token_lock
    if _cached_token and time.time() < _expires_at - TOKEN_REFRESH_MARGIN:
        return _cached_token

    # Criado aqui, e não no import, para ficar no event loop que está rodando.
    if _token_lock is None:
        _token_lock = asyncio.Lock()

    # O lock evita que várias requisições simultâneas peçam token ao mesmo tempo.
    async with _token_lock:
        if _cached_token and time.time() < _expires_at - TOKEN_REFRESH_MARGIN:
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
                _expires_at = time.time() + token_data.get("expires_in", 3600)
                return _cached_token
            else:
                print(f"Error fetching token: {response.text}")
                return None
