# FE Build
FROM node:18-slim AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


#BE Build
FROM python:3.12-slim AS python-builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY requirements.txt .

RUN uv venv /app/venv
RUN . /app/venv/bin/activate && uv pip install -r requirements.txt


# Final Build
FROM python:3.12-slim

LABEL org.opencontainers.image.authors="Sombra Team(https://github.com/Sombra-MLET2)"

WORKDIR /opt/app/

COPY --from=python-builder /app/venv /opt/app/venv
COPY --from=frontend-builder /app/frontend/build /opt/app/frontend/build

COPY src ./src
COPY datathon.db .
COPY data/chroma_storage ./data/chroma_storage
COPY model/train ./model/train

ENV PATH="/opt/app/venv/bin:$PATH"
ENV PYTHONPATH="/opt/app"

EXPOSE 80
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
