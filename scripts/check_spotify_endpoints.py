"""Testa quais endpoints do Spotify o app consegue usar com as credenciais do .env.

Em 27/11/2024 o Spotify bloqueou Audio Features, Audio Analysis,
Recommendations e Related Artists para apps novos. Este script mostra
se o seu app ainda tem acesso a eles.

Uso (na raiz do repositório): python scripts/check_spotify_endpoints.py
"""
import base64
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

API = "https://api.spotify.com/v1"


def get_token(client_id, client_secret):
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = httpx.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    )
    if response.status_code != 200:
        sys.exit(f"Não consegui o token ({response.status_code}): {response.text}")
    return response.json()["access_token"]


def main():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit("Defina SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET no .env")

    client = httpx.Client(
        base_url=API,
        headers={"Authorization": f"Bearer {get_token(client_id, client_secret)}"},
        timeout=15,
    )

    # Busca uma música para ter IDs reais; a busca continua liberada para todos.
    search = client.get("/search", params={"q": "Bohemian Rhapsody Queen", "type": "track", "limit": 1})
    if search.status_code != 200:
        sys.exit(f"A busca falhou ({search.status_code}): {search.text}")
    track = search.json()["tracks"]["items"][0]
    track_id = track["id"]
    artist_id = track["artists"][0]["id"]
    print(f"Música de teste: {track['name']} - {track['artists'][0]['name']}\n")

    checks = [
        ("Busca (referência)", "/search?q=queen&type=track&limit=1", False),
        ("Detalhes da música", f"/tracks/{track_id}", False),
        ("Audio Features", f"/audio-features/{track_id}", True),
        ("Audio Analysis", f"/audio-analysis/{track_id}", True),
        ("Recommendations", f"/recommendations?seed_tracks={track_id}&limit=1", True),
        ("Related Artists", f"/artists/{artist_id}/related-artists", True),
    ]

    blocked = []
    for name, path, restricted in checks:
        status = client.get(path).status_code
        ok = status == 200
        label = "OK" if ok else f"FALHOU ({status})"
        note = "  <- restrito desde 11/2024" if restricted else ""
        print(f"{name:<22} {label}{note}")
        if restricted and not ok:
            blocked.append(name)

    print()
    if not blocked:
        print("O app tem acesso aos endpoints restritos. O plano da etapa C pode seguir.")
    else:
        print(f"Sem acesso a: {', '.join(blocked)}.")
        print("A etapa C precisa de outra fonte de dados (ex.: Last.fm, ListenBrainz).")


if __name__ == "__main__":
    main()
