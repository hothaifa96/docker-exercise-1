# NotesApp – Docker Practice Lab

A full-stack Notes application built for **DevOps students** to practice:
- Building Docker images from Dockerfiles
- Running containers manually with `docker build` & `docker run`
- Passing environment variables to containers
- Connecting multiple containers via a shared Docker network

---

## Architecture

```
┌─────────────────┐     HTTP      ┌──────────────────┐     SQL      ┌─────────────┐
│  Frontend        │ ──────────► │   Backend (Flask) │ ──────────► │  MySQL DB   │
│  React + Nginx   │             │   Python 3.11     │             │  MySQL 8    │
│  port: 3000      │             │   port: 5000      │             │  port: 3306 │
└─────────────────┘             └──────────────────┘             └─────────────┘
```

---

## 🎯 Your Task

You must run the entire app using **only `docker build` and `docker run` commands**.  
No `docker-compose`. No shortcuts. Read the instructions carefully.

---

## Project Structure

```
.
├── backend/
│   ├── app.py              # Flask API (CRUD + search)
│   ├── requirements.txt
│   └── Dockerfile          # ← Study this!
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile          # ← Study this!
├── db/
│   └── init.sql            # DB schema (auto-applied by MySQL image)
├── .env.example            # ← ENV variables you need to find
└── README.md
```

---

##  Step 1 – Find the Environment Variables

Open `.env.example`. It lists all `???` variables you need to supply.  
You must decide the values yourself. Fill them in before proceeding.

**Questions to answer:**
- What `DB_HOST` should the backend use to reach MySQL when both run in the same Docker network?
- What should `REACT_APP_API_URL` be so the browser can reach the backend?

---

##  Step 2 – Create a Docker Network

All containers must communicate. Create a shared bridge network:##  Step 3 – Run MySQL

```bash
docker run -d \
  --name notes-db \
  --network  \
  -e  \
  -e  \
  -e  \
  -e  \
  -v  \
  -p 3306:3306 \
  mysql:8
```

> **Hint:** The container name you use with `--name` is the hostname other containers can use to reach it.

Wait ~15 seconds for MySQL to initialize before the next step.

---

##  Step 4 – Build & Run the Backend
```bash
curl http://localhost:5000/health
# Expected: {"status": "ok"}
```

---

## Step 5 – Build & Run the Frontend

The `REACT_APP_API_URL` is baked into the image at **build time** (not runtime).  
You must pass it as a **build argument**.

**Build:**
```bash
docker build \
  --build-arg REACT_APP_API_URL=<???> \
  -t notes-frontend \
  ./frontend
```

> 💡 **Hint:** The browser (your laptop) makes requests to the backend. `localhost:5000` is exposed from Step 4.


Open your browser at: **http://localhost:port**

---
