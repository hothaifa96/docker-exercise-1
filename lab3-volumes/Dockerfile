# ============================================================
# Lab 3 — Volumes Dockerfile
# Concept: VOLUME instruction, data directory creation
# ============================================================

FROM python:3.11-slim

LABEL maintainer="Docker Labs"
LABEL app="notes-app"
LABEL description="Note-taking app — demonstrates Docker volumes"

WORKDIR /app

# Install dependencies first (layer cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Create the data directory that will be used for volume mount
# This ensures the directory exists even without a volume
RUN mkdir -p /data

# VOLUME instruction — tells Docker this path is meant for external storage
# When a volume IS mounted here, it overrides this directory
# When NO volume is mounted, data goes here (but is lost with the container)
VOLUME ["/data"]

ENV DATA_DIR=/data
ENV PORT=5000

EXPOSE 5000

CMD ["python3", "app.py"]
