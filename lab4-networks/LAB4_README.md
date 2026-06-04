# 🌐 Lab 4 — Docker Networks + Frontend / Backend

## 🎯 Concept
By default, containers are isolated — they can't talk to each other.  
Docker networks let containers **communicate by name** (container DNS).  
This lab builds a two-container app: a Python Flask backend API and  
a JavaScript frontend served by nginx.

---

## 📋 Network Types Reference

| Driver | Use case |
|--------|---------|
| `bridge` | Default for single-host container communication |
| `host` | Container shares host network (no isolation) |
| `none` | No networking — fully isolated |
| `overlay` | Multi-host (Docker Swarm) |
| `macvlan` | Container gets its own MAC/IP on the LAN |

---

## 🔑 Network Commands

```bash
docker network create     # Create a network
docker network ls         # List all networks
docker network inspect    # Detailed network info
docker network connect    # Attach a running container to a network
docker network disconnect # Detach a container from a network
docker network rm         # Remove a network
docker network prune      # Remove unused networks
```

---

## 🏗 Architecture

```
Browser
  │
  │  http://localhost:3000
  ▼
┌─────────────────┐       ┌────────────────────┐
│   FRONTEND      │       │    BACKEND         │
│   nginx:alpine  │       │   Python Flask     │
│   port 3000:80  │       │   port 5000:5000   │
│                 │       │                    │
│  serves HTML+JS │       │  /api/tasks (JSON) │
└────────┬────────┘       └────────────────────┘
         │  JS calls backend via browser         
         │  → http://localhost:5000/api/tasks    
         │                                       
         └──── Both on: tasks-network ──────────┘
               (Docker bridge network)
```

> **Note:** The JS in the browser calls the backend via the **exposed host port** (`localhost:5000`), not via container DNS. Container DNS is used for server-to-server communication (see Lab 6).

---

## 🚀 PART 1 — Default Bridge Network (No custom network)

```bash
# The default bridge network does NOT support container DNS
docker network ls
docker network inspect bridge

# Run two containers on the default bridge
docker run -d --name container-a alpine sleep 60
docker run -d --name container-b alpine sleep 60

# Try to ping container-a BY NAME from container-b
docker exec -it container-b ping container-a
# FAILS — no DNS on default bridge!

# But you CAN ping by IP
docker inspect container-a | grep IPAddress
# docker exec -it container-b ping <ip>

docker stop container-a container-b && docker rm container-a container-b
```

---

## 🚀 PART 2 — Create a Custom Bridge Network

```bash
# Create a custom bridge network
docker network create tasks-network

# Inspect it
docker network inspect tasks-network

# Custom bridge networks support CONTAINER DNS!
# Containers can reach each other by name
docker run -d --name net-a --network tasks-network alpine sleep 60
docker run -d --name net-b --network tasks-network alpine sleep 60

# Ping by NAME — works!
docker exec -it net-b ping net-a -c 3

docker stop net-a net-b && docker rm net-a net-b
```

---

## 🚀 PART 3 — Build and Run the Frontend/Backend App

### Step 3.1 — Build both images

```bash
cd lab4-networks

# Build backend image
docker build -t tasks-backend:v1 ./backend

# Build frontend image
docker build -t tasks-frontend:v1 ./frontend
```

### Step 3.2 — Run the backend

```bash
docker run -d \
  --name backend \
  --network tasks-network \
  -p 5000:5000 \
  tasks-backend:v1

# Test the backend directly
curl http://localhost:5000/api/tasks
curl http://localhost:5000/api/health
```

### Step 3.3 — Run the frontend

```bash
docker run -d \
  --name frontend \
  --network tasks-network \
  -p 3000:80 \
  tasks-frontend:v1
```

### Step 3.4 — Open the app

Visit **http://localhost:3000** in your browser.  
You should see the Task Manager app. Add, complete, and delete tasks!

### Step 3.5 — Verify network communication

```bash
# Both containers are on the same network
docker network inspect tasks-network

# From the frontend container, ping the backend by name
docker exec -it frontend ping backend -c 3

# The backend container sees the frontend too
docker exec -it backend ping frontend -c 3
```

---

## 🚀 PART 4 — Network Isolation

```bash
# Create an isolated network
docker network create isolated-network

# A container on isolated-network CANNOT reach containers on tasks-network
docker run -d --name isolated-app --network isolated-network alpine sleep 60

# Try to ping the backend (on tasks-network) — should fail
docker exec -it isolated-app ping backend -c 3

docker stop isolated-app && docker rm isolated-app
docker network rm isolated-network
```

---

## 🚀 PART 5 — Attach a Container to Multiple Networks

```bash
# Create a second network
docker network create second-network

# A container can be on MULTIPLE networks simultaneously
docker network connect second-network backend

# Verify
docker inspect backend | grep -A 20 '"Networks"'

# Disconnect
docker network disconnect second-network backend
docker network rm second-network
```

---

## 🧹 Cleanup

```bash
docker stop frontend backend
docker rm frontend backend
docker network rm tasks-network
```

---

## 🎓 Exercises

1. Run both containers **without** `--network tasks-network`. Try to connect from frontend to backend by name — what happens?
2. Use `docker network inspect tasks-network` to find the IP addresses of both containers.
3. Use `docker exec -it backend env` to see the environment variables inside the backend.
4. **Add** a `GET /api/stats` endpoint to the backend that returns task statistics. Update the frontend to show them.
5. Connect the backend to **two networks** simultaneously. Verify with `docker inspect`.

---

## 🏆 Bonus Challenges

- **B1:** Add a third container (a Python script) that connects to the backend API on the Docker network and prints task stats every 5 seconds.
- **B2:** Use `--network host` on Linux and see how it differs from bridge networking.
- **B3:** Add a `--link` (legacy) connection and compare it to the modern custom network approach.
