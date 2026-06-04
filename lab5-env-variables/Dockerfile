# ============================================================
# Lab 5 — Environment Variables Dockerfile
# Concept: ENV defaults, ARG build vars, runtime overrides
# ============================================================

FROM python:3.11-slim

LABEL maintainer="Docker Labs"
LABEL app="config-app"
LABEL description="Demonstrates Docker environment variables"

# ARG — build-time only (not available when container runs)
# Override: docker build --build-arg APP_VERSION=2.0 .
ARG APP_VERSION=1.0

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# ENV — these are the DEFAULT values baked into the image
# They CAN be overridden at runtime with -e or --env-file
# Think of them as "default configuration for the image"
ENV APP_NAME="Docker Config App"
ENV ENVIRONMENT=production
# ⚠️  LAB TEACHING MOMENT: Hardcoding secrets in ENV is BAD PRACTICE!
# This is intentionally insecure to show what NOT to do.
# In production: use Docker Secrets, AWS SSM, or Vault — NOT ENV.
# override safely at runtime: docker run -e SECRET_KEY="$(openssl rand -hex 32)"
ENV SECRET_KEY=changeme-insecure
ENV DATABASE_URL=sqlite:///app.db
ENV MAX_ITEMS=100
ENV FEATURE_DARK_MODE=false
ENV ADMIN_EMAIL=admin@example.com
ENV PORT=5000

# Use the ARG to set an ENV — this bridges build-time → runtime
ENV APP_VERSION=${APP_VERSION}

# Python-specific: don't write .pyc files, flush output immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python3", "app.py"]
