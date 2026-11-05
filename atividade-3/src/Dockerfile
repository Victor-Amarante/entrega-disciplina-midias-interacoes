# Uma imagem só: o Next é exportado como site estático e servido pelo FastAPI,
# então o experimento inteiro fica num link.

FROM node:22-alpine AS frontend
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npx next build

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /bin/uv
WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev
COPY backend/app ./app
COPY --from=frontend /app/out /app/frontend/out
ENV PASTA_ESTATICA=/app/frontend/out \
    PASTA_DADOS=/data \
    PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["sh", "-c", ".venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
