# ============================================================
# Lab 6 — Worker Dockerfile
# No EXPOSE — this container has no server, only outbound Redis
# ============================================================

FROM python:3.11-slim

LABEL app="lab6-worker"
LABEL role="background-worker"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .

RUN mkdir -p /logs

ENV PYTHONUNBUFFERED=1

CMD ["python3", "worker.py"]
