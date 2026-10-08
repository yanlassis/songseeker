from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.spotify_client import get_spotify_token

app = FastAPI(title="Songseeker MVP")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Songseeker API"}

@app.get("/api/token-status")
async def check_token():
    token = await get_spotify_token()
    if token:
        return {"status": "ok"}
    return JSONResponse(
        status_code=503,
        content={"status": "error", "message": "Failed to retrieve token. Verifique o arquivo .env"},
    )
