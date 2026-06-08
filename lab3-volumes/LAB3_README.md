# Lab 3 — Docker Volumes & Multi-Container Apps

> **Goal:** Run a 3-service application that shares data through a Docker volume.
> You will **write every Dockerfile yourself** — the code is provided, the containers are your job.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Docker Volume: logs-data              │
│                    (mounted path: /logs)                 │
└───────────┬─────────────────────────┬────────────────────┘
            │ writes                  │ reads (read-only)
            ▼                         ▼
  ┌─────────────────┐       ┌──────────────────┐
  │   WORKER        │       │   BACKEND        │
  │  (Python)       │       │  (Express API)   │
  │  generator.py   │       │  server.js       │
  │  no port        │       │  port 4000       │
  └─────────────────┘       └────────┬─────────┘
                                     │ REST API
                                     ▼
                            ┌──────────────────┐
                            │   FRONTEND       │
                            │  (nginx + HTML)  │
                            │  port 3000 → 80  │
                            └──────────────────┘
                                     ▲
                               user's browser
```

### What each service does

| Service  | Language | Role |
|----------|----------|------|
| **worker**   | Python  | Writes a random log line every 2 seconds to `/logs/app-YYYY-MM-DD.log` |
| **backend**  | Express | Reads `/logs` and exposes `GET /files` and `GET /files/:name` |
| **frontend** | nginx   | Serves a web UI — shows files, click to view content live |

---

## Part 1 — Understand the code

Before writing any Dockerfile, explore the source files:

```bash
# Look at what the worker writes
cat worker/generator.py

# Look at the API endpoints
cat backend/server.js

# Look at the frontend
cat frontend/index.html
cat frontend/app.js
```

**Questions to answer:**
1. What environment variable controls where the worker writes logs?
2. What two API routes does the backend expose?
3. What URL does `app.js` use to reach the backend?

---

## Part 2 — Write the Dockerfiles


---

### Exercise 2.1 — Worker Dockerfile

Create `worker/Dockerfile`.

**What it needs to do:**
- Start from a small Python base image
- Set a working directory
- Copy `generator.py` into the image
- Run the script when the container starts


>  No `pip install` needed — only Python standard library is used.

---

### Exercise 2.2 — Backend Dockerfile

Create `backend/Dockerfile`.

**What it needs to do:**
- Start from a Node.js base image
- Set a working directory
- Copy `package.json` first and run `npm install`
- Copy the rest of the source
- Expose port 4000
- Start the server

> Why copy `package.json` before the rest? Think about Docker layer caching.

---

### Exercise 2.3 — Frontend Dockerfile

Create `frontend/Dockerfile`.

**What it needs to do:**
- Start from nginx
- Copy `index.html` and `app.js` into the nginx web root
- Copy `nginx.conf` to replace the default nginx configuration
- Expose port 80

> nginx already has a default `CMD` in its base image — you don't need to add one.

---

## Part 3 — Build the images

Once your Dockerfiles are written, build all three images

Verify they exists
---

## Part 4 — Create the shared infrastructure

### Step 4.1 — Create a named volume


This volume is the **shared folder** that worker writes to and backend reads from.

Inspect it:
```bash
docker volume inspect logs-data
```

### Step 4.2 — Create a Docker network

```bash
docker network create lab3-network
```

All containers join this network so they can reach each other **by container name**.

---

## Part 5 — Run the containers

**Order matters** — start worker first, then backend, then frontend.

### Step 5.1 — Start the worker

Watch it writing logs:

### Step 5.2 — Start the backend

Test the API:
```bash
curl http://localhost:port/health
curl http://localhost:port/files
```

### Step 5.3 — Start the frontend


Open your browser: **http://localhost:3000**

You should see the log files listed on the left. Click any file to read it. It auto-refreshes every 4 seconds.

---

## Part 6 — Verify & Explore

```bash
# See all 3 containers running
docker ps

# See the volume usage
docker volume inspect logs-data

# Enter the worker to inspect the /logs folder
docker exec -it worker ls /logs

# Enter the backend and check the same volume
docker exec -it backend ls /logs
```

**Questions:**
1. Do both containers see the same files in `/logs`?
2. What happens to the logs if you stop and restart the worker?
3. What happens if you remove the worker container — do the files survive?

---

## Part 7 — Cleanup

```bash
# Stop all containers
docker stop worker backend frontend

# Remove containers
docker rm worker backend frontend

# Remove images
docker rmi lab3-worker lab3-backend lab3-frontend

# Remove the network
docker network rm lab3-network

# Keep or remove the volume (remove = logs lost)
docker volume rm logs-data
```

---

## Bonus Challenges

### Bonus 1 — Volume persistence
Remove the worker container, create a new one from the same image. Do the old logs still exist?

### Bonus 2 — Push your images to Docker Hub


### Bonus 3 — Bind mount instead of named volume

## Dockerfile Cheat Sheet

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM`      | Base image | `FROM node:18-alpine` |
| `WORKDIR`   | Set working directory | `WORKDIR /app` |
| `COPY`      | Copy files into image | `COPY . .` |
| `RUN`       | Run a command at build time | `RUN npm install` |
| `EXPOSE`    | Document the port | `EXPOSE 4000` |
| `ENV`       | Set environment variable | `ENV PORT=4000` |
| `CMD`       | Default command at runtime | `CMD ["node", "server.js"]` |

## Volume & Network Cheat Sheet

```bash
docker volume create <name>          # Create a named volume
docker volume ls                     # List volumes
docker volume inspect <name>         # Inspect a volume
docker volume rm <name>              # Remove a volume

docker network create <name>         # Create a network
docker network ls                    # List networks
docker network inspect <name>        # Inspect a network

# Mount a volume when running a container
docker run -v <volume>:<path> ...         # named volume
docker run -v /host/path:<path> ...       # bind mount
docker run -v <volume>:<path>:ro ...      # read-only
```
