import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes import router as api_router
from .database import engine, SessionLocal
from .models import Base, create_initial_data

app = FastAPI()

frontend_path = os.path.join(os.path.dirname(__file__), '../../frontend')
print("Frontend directory path:", frontend_path)

# EN: Include API routes for handling observations and other resources
# BR: Incluir rotas da API para lidar com observações e outros recursos
app.include_router(api_router, prefix="/api")

# EN: Creates tables / BR: Cria tabelas
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    # EN: Creates new BD session / Cria nova sessiao de banco de dados
   db = SessionLocal()
   try:
      create_initial_data(db)
      print("Database initialised and initial data created.")
   finally:
      db.close()

# EN: Serve static files (CSS, JS, images) directly from the "frontend" folder
# BR: Servir arquivos estáticos (CSS, JS, imagens) diretamente da pasta "frontend"
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# EN: Serve the SPA HTML file (index.html) from the frontend folder
# BR: Servir o arquivo HTML da SPA (index.html) da pasta frontend
@app.get("/", response_class=FileResponse)
async def read_index():
    # EN: Returning the index.html file to the user
    # BR: Retornando o arquivo index.html para o usuário
    return FileResponse(os.path.join(frontend_path, "index.html"))

from fastapi.responses import FileResponse

@app.get("/new_observation", response_class=FileResponse)
async def serve_new_observation():
    return FileResponse(os.path.join(frontend_path, "index.html"))
