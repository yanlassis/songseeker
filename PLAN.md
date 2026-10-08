# Songseeker - Plano de Desenvolvimento

## 1. Stack e API
- **API Musical**: Spotify Web API (Client Credentials Flow). Foco em metadados ricos e Audio Features.
- **Backend**: Python com FastAPI e HTTPX.
- **Banco de Dados/Cache**: SQLite (SQLModel).
- **Frontend**: HTML, CSS e JS (com HTMX ou Vanilla JS).
- **Design/UI**: Utilizar a skill `impeccable` do Antigravity.

## 2. Estrutura de Pastas
- `backend/`: FastAPI, integração Spotify e recomendação.
- `frontend/`: UI focado em covers (arquivos estáticos).
- `.env`: Segredos e chaves de API.

## 3. Etapas
- [x] Etapa A: Init repo + Spotify Auth
- [ ] Etapa B: Cache SQLite
- [ ] Etapa C: Lógica de recomendação
- [ ] Etapa D: Frontend
