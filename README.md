# Songseeker

O Songseeker é uma aplicação web simples que te ajuda a descobrir novas músicas parecidas com as que você já gosta. A ideia principal é usar os dados de comunidade do Last.fm para achar recomendações reais, e a API do Spotify para renderizar as capas e permitir que você escute os previews direto na tela.

## Como rodar localmente

1. Configure o ambiente:
   Renomeie o arquivo `.env.example` para `.env` e preencha com as suas chaves geradas:

```text
SPOTIFY_CLIENT_ID=sua_chave_aqui
SPOTIFY_CLIENT_SECRET=sua_chave_aqui
LASTFM_API_KEY=sua_chave_aqui
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Suba o servidor:

```bash
uvicorn backend.main:app --reload
```
