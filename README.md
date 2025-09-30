# FocusEd Backend (FastAPI + SQLite)
**EN:** Main API for observations, teachers, departments, focus areas, and PDF export. Talks to `focused-mailer` (email) and `focused-renderer` (PDF).  
**BR:** API principal para observações, professores, departamentos, focos e exportação em PDF. Comunica com `focused-mailer` (e-mail) e `focused-renderer` (PDF).

## Quick Start (Docker)
```bash
# EN: 1) Create the shared Docker network (only once)
# BR: 1) Criar a rede Docker compartilhada (apenas uma vez)
docker network create focused-net || true

# EN: 2) Build the backend image
# BR: 2) Construir a imagem do backend
docker build -t focused-backend:0.1.0 .

# EN: 3) Run the container on port 8000
# BR: 3) Executar o contêiner na porta 8000
docker run --name backend --rm   --env-file .env   --network focused-net   -p 8000:8000   focused-backend:0.1.0
```

- **Swagger / OpenAPI:** <http://localhost:8000/docs>  
- **ReDoc:** <http://localhost:8000/redoc>  
- **Health:** `GET /health`

## Environment
See `.env.example`. Key settings:
- `MAILER_URL` (e.g., `http://mailer:8001`)
- `MAILER_API_KEY` (must match mailer)
- `RENDERER_URL` (e.g., `http://renderer:8002`)

## Architecture
```mermaid
graph TB
  FE[Frontend (Nginx :80)] -->|/api proxy (CRUD: GET/POST/PUT/DELETE)| BE[Backend (FastAPI :8000)]
  BE -->|X-API-KEY auth| M[Mailer (FastAPI :8001)]
  M -->|POST /render| R[Renderer (WeasyPrint :8002)]
  M -->|Send email| SG[(SendGrid API)]
  BE -->|SQLite file (app.db)| DB[(SQLite)]
```

**External API:** SendGrid (email delivery).

## API Overview (Key Endpoints)
| Method | Path                   | Description                                |
|-------:|------------------------|--------------------------------------------|
| GET    | /health                | Health probe                               |
| GET    | /api/observations      | List (filters: `teacher_id`, `department_id`, `focus_area_id`) |
| POST   | /api/observations      | Create observation                         |
| GET    | /api/observations/{id} | Retrieve one                               |
| PUT    | /api/observations/{id} | Update                                     |
| DELETE | /api/observations/{id} | Delete                                     |
| GET    | /api/teachers          | List teachers                              |
| GET    | /api/departments       | List departments                           |
| GET    | /api/focus             | List focus areas                           |
| GET    | /api/pdf/{id}          | Generate & return PDF (application/pdf)    |

**EN:** Backend may trigger the mailer to email a PDF (when requested).  
**BR:** O backend pode acionar o mailer para enviar um PDF por e-mail (quando solicitado).

## Minimal Examples
**Create observation**
```bash
curl -sS -X POST http://localhost:8000/api/observations   -H "Content-Type: application/json"   -d '{
    "Observation_Teacher": 1,
    "Observation_Class": "9K",
    "Observation_Department": 2,
    "Observation_Focus": 9,
    "Observation_Strengths": "Clear explanations",
    "Observation_Weaknesses": "Pacing",
    "Observation_Comments": "Good rapport"
  }'
```

**Get PDF**
```bash
curl -fL http://localhost:8000/api/pdf/1 -o obs-1.pdf
```

## Troubleshooting
- **Email not sent:** check logs for a `notify` flag, ensure `MAILER_URL` is reachable on `focused-net`, and `MAILER_API_KEY` matches in both backend and mailer.  
- **405 on `/api/pdf/{id}`:** use **GET** (HEAD may be disallowed).  
- **Renderer glyph issues:** confirm renderer is healthy and has fonts (e.g., DejaVu).

## Development Notes
- **EN:** Keep short EN/PT-BR comments in public code.  
- **BR:** Mantenha comentários curtos EN/PT-BR no código público.

## License
MIT — see `LICENSE`.

## Contributing
See `CONTRIBUTING.md`.