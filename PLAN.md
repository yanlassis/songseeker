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
- [x] Etapa B: Cache SQLite
- [x] Etapa C: Lógica de recomendação (Last.fm)
- [ ] Etapa D: Frontend

## 4. Regras de Colaboração (Git & Agents)
Atenção agentes: O desenvolvimento deste projeto é colaborativo entre o Yan e o seu primo. Siga estas regras estritamente:
1. **Branching e Pull Requests:** O primo (e seu respectivo agente) **NÃO** deve fazer push diretamente na branch `main`. Todo o trabalho dele deve ser feito em branches separadas (ex: `feature/nova-ui`, `fix/bug-spotify`). Após finalizar, deve-se criar um **Pull Request (PR)** para que o Yan avalie e faça o merge.
2. **Sincronia de Progresso:** Toda vez que houver um avanço significativo, este arquivo `PLAN.md` ou o histórico de commits deve ser atualizado para que ambos os agentes tenham sempre o contexto atualizado do que já foi feito e do que falta.
3. **Leia antes de agir:** Agentes, ao iniciarem a sessão, leiam o `PLAN.md` para entenderem em qual etapa o projeto parou.
