# ============================================================
# Lab 6 — Frontend Dockerfile
# nginx:alpine serves the static Message Board UI
# ============================================================

FROM nginx:alpine

LABEL app="lab6-frontend"
LABEL role="frontend-static"

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html/

EXPOSE 80
