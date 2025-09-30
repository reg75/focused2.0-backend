# EN: Small, reliable base / BR: Base pequena e confiável
FROM python:3.11-slim

# EN: System deps (curl for healthcheck) / BR: Dependências do sistema (curl p/ healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# EN: Copy requirements / Copiar requirements
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip


# EN: Install dependencies / BR: Instalar dependências
RUN pip install --no-cache-dir -r /app/requirements.txt

# EN: Copy backend code / BR: Copiar código do backend
COPY app /app/app

# EN: Expose FastAPI port / BR: Expor porta do FastAPI
EXPOSE 8000

# EN: Healthcheck hits /health / BR: Healthcheck consulta /health
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fsS http://127.0.0.1:8000/health || exit 1

# EN: Run server / BR: Executar o servidor
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
