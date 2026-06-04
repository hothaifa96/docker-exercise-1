# ============================================================
# Lab 4 — Frontend Dockerfile
# Concept: Serving static files with nginx inside Docker
# ============================================================

# nginx:alpine is tiny (~7 MB) — perfect for serving static files
FROM nginx:alpine

LABEL app="tasks-frontend"
LABEL role="frontend-static"

# Remove the default nginx welcome page
RUN rm -rf /usr/share/nginx/html/*

# Copy our HTML + JS into nginx's web root
COPY index.html /usr/share/nginx/html/
COPY app.js     /usr/share/nginx/html/

# EXPOSE 80 — nginx listens on port 80 by default
EXPOSE 80

# CMD is inherited from nginx:alpine — it starts nginx automatically
# You could override it explicitly:
# CMD ["nginx", "-g", "daemon off;"]
