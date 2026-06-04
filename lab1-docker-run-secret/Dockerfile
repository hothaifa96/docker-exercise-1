# ============================================================
# Lab 1 — Secret Word Hunt Image
# Concept: Dockerfile basics (covered in depth in Lab 2)
# ============================================================

# Step 1: FROM — Choose a base image from Docker Hub
#         ubuntu:22.04 gives us apt-get to install extra tools
FROM ubuntu:22.04

# Step 2: LABEL — Add metadata to your image (optional but good practice)
LABEL maintainer="Docker Labs"
LABEL description="Secret Word Hunt — find the hidden word inside this container"
LABEL lab="Lab 1 - Docker Run"

# Step 3: RUN — Execute shell commands during the BUILD phase
#         Here we install python3 and nodejs so the hunt scripts work
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

# Step 8: CMD — Default command when the container starts
#         sleep infinity keeps it alive so we can exec into it
CMD ["sleep", "infinity"]
