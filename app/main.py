import os
import pathlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .routes import router as api_router
from .database import engine, SessionLocal
from .models import Base, create_initial_data

# EN: Resolve project root and frontend path (../frontend)
# BR: Resolver raiz do projeto e caminho do frontend (../frontend)
app_dir = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = app_dir.parent.parent
FRONTEND_PATH = PROJECT_ROOT / "frontend"

print(f"Calculated Frontend directory path: {FRONTEND_PATH}")

app = FastAPI()

# EN: Health endpoint for Docker healthcheck / BR: Endpoint de saúde para o Docker
@app.get("/health")
def health():
    return {"status": "ok"}

# EN: Load .env early (once)
# BR: Carregar .env cedo (uma vez)
try:
    from dotenv import load_dotenv 
    BACKEND_DIR = app_dir.parent
    env_path = BACKEND_DIR / ".env" 
    print(f"DEBUG: Attempting to load .env from: {env_path.resolve()}") # Debug
    load_dotenv(dotenv_path=env_path, override=False)
    key = os.getenv("MAILER_API_KEY", "")
    key_preview = (key[:4] + "…" + str(len(key))) if key else "<EMPTY>"
    print(f"[env] loaded={env_path.exists()} MAILER_URL={os.getenv('MAILER_URL')} MAILER_API_KEY={key_preview}")
except Exception as e:
    print("[env] dotenv not loaded:", e)

# EN: Creates tables / BR: Cria tabelas
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    # EN: Create DB session and seed initial data
    # BR: Criar sessão de BD e popular dados iniciais
    db = SessionLocal()
    try:
        create_initial_data(db)
        print("Database initialised and initial data created.")
    finally:
        db.close()

# EN: Include API routes / BR: Incluir rotas da API
app.include_router(api_router, prefix="/api")

# EN: Mount static frontend to root (/) for SPA. html=True handles / and client-side routes.
# BR: Montar frontend estático na raiz (/) para SPA. html=True trata / e rotas do lado do cliente.
if FRONTEND_PATH.is_dir():
    app.mount(
        "/static", 
        StaticFiles(directory=str(FRONTEND_PATH), html=False), 
        name="static-assets"
    )
else:
    print(f"[frontend] WARNING: Frontend path not found at {FRONTEND_PATH}; static mount skipped")

# EN: Handle the bare root (/) explicitly, which also serves index.html
@app.get("/", include_in_schema=False)
async def serve_root_index():
    index_file = FRONTEND_PATH / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"detail": "Not Found"}, 404

# EN: SPA Fallback: Catch all remaining GET requests and serve index.html.
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa_index(full_path: str):
    index_file = FRONTEND_PATH / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"detail": "Not Found"}, 404