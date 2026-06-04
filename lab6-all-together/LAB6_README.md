# 🚀 Lab 6 — All Together (Docker Compose)

## 🎯 Concept
Combine **everything** from Labs 1–5 into one full-stack application managed  
by **Docker Compose** — the tool for defining and running multi-container apps  
from a single `docker-compose.yml` file.

---

## 📋 What Is Docker Compose?

Instead of running many `docker run` commands manually, Compose lets you:
- Define all services in ONE file (`docker-compose.yml`)
- Start everything with ONE command: `docker compose up`
- Stop everything with ONE command: `docker compose down`

---

## 🏗 Architecture — Message Board App

```
Browser
  │
  │  http://localhost:3000
  ▼
┌──────────────────┐    frontend-network
│   FRONTEND       │ ─────────────────────────────┐
│   nginx:alpine   │                               │
│   port 3000:80   │                 ┌─────────────▼──────────┐
└──────────────────┘                 │   BACKEND               │
                                     │   Python Flask          │
                                     │   port 5000:5000        │
                                     │   /api/messages         │
                                     └─────────┬───────────────┘
                                               │  backend-network
                                     ┌─────────▼───────────────┐
                                     │   REDIS                  │
                                     │   redis:7-alpine         │
                                     │   Named Volume: redis-data│
                                     └─────────┬───────────────┘
                                               │  backend-network
                                     ┌─────────▼───────────────┐
                                     │   WORKER                 │
                                     │   Python script          │
                                     │   Polls Redis queue      │
                                     │   Named Volume: logs     │
                                     └─────────────────────────┘
```

### Concepts Used in This Lab

| Lab | Concept | Where |
|-----|---------|-------|
| Lab 1 | docker run / exec | `docker compose exec` |
| Lab 2 | Dockerfiles | 3 custom Dockerfiles |
| Lab 3 | Volumes | `redis-data`, `worker-logs` |
| Lab 4 | Networks | `frontend-network`, `backend-network` |
| Lab 5 | Env Variables | `.env` file + `environment:` in compose |
| Lab 6 | Compose | `docker-compose.yml` orchestrates all |

---

## 🔑 Docker Compose Commands

```bash
docker compose up           # Start all services (foreground)
docker compose up -d        # Start all services (detached / background)
docker compose down         # Stop + remove containers and networks
docker compose down -v      # Also remove volumes (data deleted!)
docker compose ps           # List service status
docker compose logs         # View logs for all services
docker compose logs backend # View logs for one service
docker compose logs -f      # Follow (live) logs
docker compose exec backend bash  # Shell into a running service
docker compose build        # Build/rebuild images
docker compose pull         # Pull latest images from Docker Hub
docker compose restart      # Restart all services
docker compose stop         # Stop (don't remove) all containers
docker compose start        # Start stopped containers
docker compose scale worker=3  # Run 3 worker instances
```

---

## 🚀 PART 1 — Start the Full Stack

```bash
cd lab6-all-together

# Copy env file and review it
cp .env.example .env

# Build all custom images and start everything
docker compose up --build -d

# Check all services are running
docker compose ps

# View combined logs from all services
docker compose logs

# Or follow one service
docker compose logs -f worker
```

Visit **http://localhost:3000** — the Message Board should be live!

---

## 🚀 PART 2 — Explore the Running Stack

```bash
# Which networks were created?
docker network ls | grep lab6

# Which volumes exist?
docker volume ls | grep lab6

# Exec into the backend
docker compose exec backend bash
env | grep -E "REDIS|APP|FLASK"
exit

# Exec into Redis and inspect data
docker compose exec redis redis-cli
> KEYS *
> LRANGE messages 0 -1
> LLEN pending_queue
> exit
```

---

## 🚀 PART 3 — Network Isolation Demo

```bash
# The frontend container is on frontend-network + backend-network
# The worker is ONLY on backend-network
# Can the frontend reach Redis directly? (It shouldn't!)
docker compose exec frontend ping redis -c 3
# Should FAIL — frontend is not on backend-network!

# Can the backend reach Redis? (It should)
docker compose exec backend ping redis -c 3
# Should SUCCEED — both on backend-network
```

---

## 🚀 PART 4 — Volume Persistence

```bash
# Post some messages via the API
curl -X POST http://localhost:5000/api/messages \
  -H "Content-Type: application/json" \
  -d '{"text": "Volumes keep data alive!", "author": "Docker Student"}'

# Stop and restart only the backend — data in Redis persists!
docker compose restart backend

curl http://localhost:5000/api/messages
# Messages are still there (stored in Redis on a named volume)

# Now stop everything BUT keep volumes
docker compose down

# Start again — messages still there!
docker compose up -d
curl http://localhost:5000/api/messages
```

---

## 🚀 PART 5 — Scale the Worker

```bash
# Run 3 worker instances processing the queue simultaneously
docker compose up -d --scale worker=3

# Watch all 3 workers in the logs
docker compose logs -f worker

# Post several messages — all 3 workers compete to process them
for i in {1..10}; do
  curl -s -X POST http://localhost:5000/api/messages \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Message $i\", \"author\": \"Load Test\"}"
done

docker compose logs worker | tail -30
```

---

## 🚀 PART 6 — Override Compose Config

```bash
# Override env vars without changing docker-compose.yml
docker compose up -d \
  -e APP_NAME="Custom Board" \
  -e FLASK_ENV=development

# Or create a docker-compose.override.yml for dev overrides
```

---

## 🧹 Cleanup

```bash
# Stop and remove containers + networks (keep volumes)
docker compose down

# Stop and remove EVERYTHING including volumes
docker compose down -v

# Remove the built images too
docker compose down -v --rmi local
```

---

## 🎓 Exercises

1. Run `docker compose up -d` and verify all 4 services are healthy with `docker compose ps`.
2. Use `docker compose exec backend env` to verify environment variables are loaded from `.env`.
3. Post 5 messages via the API and watch the worker process them with `docker compose logs -f worker`.
4. Stop the backend (`docker compose stop backend`). Try to post a message — what happens in the frontend?
5. Run `docker compose down` then `docker compose up -d` again. Are the messages still in Redis?

---

## 🏆 Bonus Challenges

- **B1:** Add a `HEALTHCHECK` to the backend and worker Dockerfiles. Watch `docker compose ps` show `(healthy)`.
- **B2:** Create a `docker-compose.override.yml` that mounts the backend source code as a bind mount for live code reloading in development.
- **B3:** Add a **5th service**: a simple Python script (`monitor.py`) that runs every 10 seconds and prints stats from the Redis queue.
- **B4:** Use `docker compose scale worker=5` and post 20 messages. Observe how the work is distributed.
- **B5:** Add a `restart: on-failure` policy to the worker and intentionally crash it. Watch Compose restart it.
