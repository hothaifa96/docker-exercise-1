# ============================================================
# Lab 4 — Backend Dockerfile
# Concept: Building an API container to be used in a network
# ============================================================

FROM python:3.11-slim

LABEL app="tasks-backend"
LABEL role="backend-api"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "app.py"]
