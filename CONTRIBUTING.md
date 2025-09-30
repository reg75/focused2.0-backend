# Contributing — FocusEd Backend
**EN:** Thanks for helping improve the FocusEd backend.  
**BR:** Obrigado por colaborar com o backend do FocusEd.

## How to work locally
```bash
# EN: Build & run with Docker
# BR: Construir e executar com Docker
docker network create focused-net || true
docker build -t focused-backend:0.1.0 .
docker run --name backend --rm \
  --env-file .env \
  --network focused-net \
  -p 8000:8000 \
  focused-backend:0.1.0
```

- **Docs:** http://localhost:8000/docs  
- **Health:** `GET /health`

## Branch & commit style
- **Branches / Ramos:** `feat/<topic>`, `fix/<bug>`, `docs/<area>`
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`)
- **PRs:** Small, focused, include a 3–5 line summary (EN/PT-BR is welcome)

## Code style / Estilo de código
- **Formatting:** [Black](https://black.readthedocs.io/)
- **Linting:** ruff (or flake8)
- **Typing:** Add type hints where practical
- **Docstrings:** Keep public endpoints with short EN/PT-BR notes  
  **BR:** Mantenha comentários curtos EN/PT-BR nos endpoints públicos

## Tests & checks / Testes e verificações
- Run container; verify `GET /health` and `/docs`.
- Add minimal tests for new routes where feasible.
- Ensure README tables reflect API changes.

## API changes / Mudanças de API
- Update `README.md` (endpoint table + examples)
- Update `CHANGELOG.md`
- Keep responses consistent (status codes, error shape)

## Security / Segurança
- Do **not** commit real secrets:
  - `.env` is ignored (keep local only)
  - `.env.example` documents required variables
- Shared secret with mailer: `MAILER_API_KEY` must match across services

## Versioning / Versionamento
- MVP uses simple tags (e.g., `0.1.0`)
- Update `CHANGELOG.md` with date and section
- Tag releases in GitHub when you cut an image

## Definition of done / Definição de pronto
- Builds & runs via Docker
- `/health` and `/docs` pass manual checks
- README updated (Quick Start, Env, Endpoints)
- Changelog entry added