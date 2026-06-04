# ============================================================
# Lab 2 — Python Flask Dockerfile
# Concept: Layer caching, slim images, best practices
# ============================================================

# STEP 1: FROM — choose a base image
#   python:3.11-slim is a minimal Debian-based Python image
#   "slim" removes unnecessary packages (~50% smaller than full)
FROM python:3.11-slim

# STEP 2: LABEL — image metadata (optional but recommended)
LABEL maintainer="Docker Labs"
LABEL app="python-flask-demo"
LABEL version="1.0"

# STEP 3: ARG — build-time variable (not available at runtime)
#   Override with: docker build --build-arg APP_VERSION=2.0 .
ARG APP_VERSION=1.0

# STEP 4: ENV — runtime environment variable
#   This IS available when the container runs
ENV APP_VERSION=${APP_VERSION}
ENV ENVIRONMENT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# STEP 5: WORKDIR — set working directory inside the image
#   Creates the directory if it doesn't exist
WORKDIR /app

# STEP 6: COPY requirements.txt FIRST (layer cache optimization!)
#   If requirements.txt hasn't changed, Docker reuses the cached layer
#   for the pip install step — saving time on rebuilds
COPY requirements.txt .

# STEP 7: RUN pip install — executed at BUILD time
#   --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# STEP 8: COPY the rest of the application source code
#   This layer changes every time you edit code
#   That's why we separate requirements.txt copy (above)
COPY . .

# STEP 9: EXPOSE — document which port the app listens on
#   This does NOT publish the port; use -p flag with docker run
EXPOSE 5000

# STEP 10: CMD — default command when the container starts
#   Use JSON array form (avoids /bin/sh -c wrapper)
#   Overridable: docker run flask-app:v1 python3 -c "print('hi')"
CMD ["python3", "app.py"]
