# ============================================================
# Lab 6 — Backend Dockerfile
# Concepts from Lab 2: layers, caching, slim image
# ============================================================

FROM python:3.11-slim

LABEL app="lab6-backend"
LABEL role="api"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=5000
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python3", "app.py"]
