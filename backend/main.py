from fastapi import FastAPI
from backend.spotify_client import get_spotify_token

app = FastAPI(title="Songseeker MVP")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Songseeker API"}

@app.get("/api/token-status")
async def check_token():
    token = await get_spotify_token()
    if token:
        return {"status": "ok", "token_preview": f"{token[:10]}..."}
    return {"status": "error", "message": "Failed to retrieve token. Verifique o arquivo .env"}
