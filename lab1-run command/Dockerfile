# ============================================================
# Lab 1-Startner — Secret Word Hunt Image
# Concept: Dockerfile basics — same as Lab 1, fresh questions
# ============================================================

# Step 1: FROM — Choose a base image
FROM ubuntu:22.04

# Step 2: LABEL — Metadata
LABEL maintainer="Docker Labs"
LABEL description="Startner Secret Hunt — find the hidden word inside this container"
LABEL lab="Lab 1-Startner - Docker Run"

# Step 3: RUN — Install python3 and nodejs so the hunt scripts work
RUN apt-get update && apt-get install -y \
    python3 \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Step 4: RUN — Create the directories the scripts will live in
RUN mkdir -p /scripts /hints

# Step 5: COPY — Copy files from your host machine INTO the image
COPY scripts/ /scripts/
COPY hints/   /hints/

# Step 6: RUN — Set permissions so scripts are executable
RUN chmod 755 /scripts/clue1.py /scripts/trivia.js

# Step 7: WORKDIR — Set the default working directory
WORKDIR /

# Step 8: CMD — Keep container alive so we can exec into it
CMD ["sleep", "infinity"]
