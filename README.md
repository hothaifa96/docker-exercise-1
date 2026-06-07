# 🐳 Docker Labs — class lab

6 hands-on labs that take you from zero to full-stack Docker proficiency.  
Each lab builds on the previous one. Work through them in order!

---

## 📚 Lab Overview

| # | Lab | Core Concept | Languages |
|---|-----|-------------|-----------|
| 1 | [Docker Run & Secret Hunt](./lab1-docker-run-secret/) | `pull`, `run`, `exec`, `ps`, `logs`, `rm` | Python, JS |
| 2 | [Building Docker Images](./lab2-basic-images/) | `Dockerfile`, `build`, `tag`, `push` | Python Flask, Java, C# |
| 3 | [Docker Volumes](./lab3-volumes/) | Named volumes, bind mounts, persistence | Python Flask |
| 4 | [Networks + Frontend/Backend](./lab4-networks/) | Bridge networks, container DNS, multi-container | Python Flask + JS |
| 5 | [Environment Variables](./lab5-env-variables/) | `ENV`, `-e`, `--env-file`, secrets | Python Flask |
| 6 | [All Together](./lab6-all-together/) | Docker Compose — full stack app | Python Flask + JS + Worker |

---

## 🛠 Prerequisites

- Docker Desktop installed and running (`docker --version`)
- Terminal / Command Prompt access
- Text editor (VS Code recommended)
- Basic command-line knowledge

---

## 🚀 Quick Start

```bash
# Verify Docker is running
docker --version
docker info

# Clone / open this workspace, then enter any lab folder
cd lab1-docker-run-secret
cat LAB1_README.md
```

---

## 🧹 Cleanup Between Labs

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Nuclear option — remove everything unused
docker system prune -f
```

---
