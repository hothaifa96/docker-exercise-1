# 💾 Lab 3 — Docker Volumes (Data Persistence)

## 🎯 Concept
By default, all data inside a container is **lost when the container is removed**.  
Volumes solve this by storing data OUTSIDE the container's writable layer.

There are two ways to persist data:
- **Named Volumes** — Docker manages the storage location (`docker volume create`)
- **Bind Mounts** — You specify an exact path on your host machine

---

## 📋 Volume Types Comparison

| Feature | Named Volume | Bind Mount |
|---------|-------------|------------|
| Managed by | Docker | You (host path) |
| Syntax | `-v myvolume:/data` | `-v /host/path:/container/path` |
| Portable? | Yes | No (host-specific path) |
| Good for | Databases, app data | Development, config files |
| Created with | `docker volume create` | Automatic (host dir must exist) |

---

## 🔑 Volume Commands

```bash
docker volume create     # Create a named volume
docker volume ls         # List all volumes
docker volume inspect    # Inspect a volume (see mount point)
docker volume rm         # Remove a volume
docker volume prune      # Remove all unused volumes
```

---

## 🐍 The App — Flask Note-Taking App

This Flask app lets you write notes that are saved to a file in `/data/notes.txt`.  
Without a volume, the notes disappear when the container is removed.  
With a volume, they persist forever — even across container restarts.

### Endpoints
- `GET /` → View all notes (HTML page)
- `POST /notes` → Add a note
- `GET /notes` → List notes (JSON)
- `DELETE /notes/<id>` → Delete a note
- `GET /export` → Download notes as a text file

---

## 🚀 PART 1 — The Problem: Data Loss Without Volumes

```bash
cd lab3-volumes

# Build the image
docker build -t notes-app:v1 .

# Run WITHOUT a volume
docker run -d --name notes-no-volume -p 5001:5000 notes-app:v1

# Add some notes
curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker volumes are important!", "author": "Student"}'

curl http://localhost:5001/notes

# Now DELETE the container
docker stop notes-no-volume
docker rm notes-no-volume

# Run a new container — notes are GONE
docker run -d --name notes-no-volume -p 5001:5000 notes-app:v1
curl http://localhost:5001/notes
# Result: empty list — data lost!

docker stop notes-no-volume && docker rm notes-no-volume
```

---

## 🚀 PART 2 — Named Volumes: Docker-Managed Persistence

```bash
# Create a named volume
docker volume create notes-data

# See the volume was created
docker volume ls

# Inspect where Docker actually stores the data
docker volume inspect notes-data

# Run the app WITH the named volume
# -v notes-data:/data  → mount 'notes-data' volume at /data inside container
docker run -d \
  --name notes-app \
  -p 5001:5000 \
  -v notes-data:/data \
  notes-app:v1

# Add some notes
curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "This note will survive container restarts!", "author": "Docker Student"}'

curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Named volumes are managed by Docker.", "author": "Docker Student"}'

curl http://localhost:5001/notes

# Kill the container
docker stop notes-app && docker rm notes-app

# Start a BRAND NEW container with the SAME volume
docker run -d \
  --name notes-app-new \
  -p 5001:5000 \
  -v notes-data:/data \
  notes-app:v1

# Notes are still there!
curl http://localhost:5001/notes

docker stop notes-app-new && docker rm notes-app-new
```

---

## 🚀 PART 3 — Bind Mounts: Host-Managed Persistence

```bash
# Create a directory on your HOST machine
mkdir -p /tmp/notes-host-data

# Mount it into the container
# $(pwd) would also work if you're in the right directory
docker run -d \
  --name notes-bind \
  -p 5001:5000 \
  -v /tmp/notes-host-data:/data \
  notes-app:v1

# Add a note
curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "I can see this file on my host machine!", "author": "Explorer"}'

# VIEW THE FILE DIRECTLY ON YOUR HOST — no container needed!
cat /tmp/notes-host-data/notes.json

# You can edit it directly on the host too!
# The running container will see the changes immediately
docker stop notes-bind && docker rm notes-bind
```

---

## 🚀 PART 4 — Read-Only Bind Mount (Configuration)

```bash
# Bind mount in READ-ONLY mode (:ro)
# Useful for config files you don't want the container to modify
docker run -d \
  --name notes-readonly \
  -p 5001:5000 \
  -v /tmp/notes-host-data:/data:ro \
  notes-app:v1

# Try to add a note — will fail because /data is read-only!
curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Can I write this?", "author": "Test"}'

docker stop notes-readonly && docker rm notes-readonly
```

---

## 🚀 PART 5 — Share a Volume Between Containers

```bash
# Create shared volume
docker volume create shared-notes

# Container 1: writer
docker run -d \
  --name notes-writer \
  -p 5001:5000 \
  -v shared-notes:/data \
  notes-app:v1

# Container 2: reader (read-only)
docker run -d \
  --name notes-reader \
  -p 5002:5000 \
  -v shared-notes:/data:ro \
  notes-app:v1

# Write through container 1
curl -X POST http://localhost:5001/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Written by container 1", "author": "Writer"}'

# Read from container 2 — same data!
curl http://localhost:5002/notes

docker stop notes-writer notes-reader
docker rm notes-writer notes-reader
```

---

## 🧹 Cleanup

```bash
# Remove volumes (WARNING: data is deleted!)
docker volume rm notes-data shared-notes
docker volume prune -f
```

---

## 🎓 Exercises

1. Run the app without a volume, add 3 notes, stop & remove the container, restart it — confirm data is lost.
2. Run the app with a named volume, add notes, restart the container — confirm data persists.
3. Use `docker volume inspect` to find where Docker stores the named volume data on your host.
4. Mount a file (not a directory) as a bind mount: `-v /tmp/myconfig.txt:/app/config.txt`.
5. Run two containers sharing the same named volume. Write from one, read from the other.

---

## 🏆 Bonus Challenges

- **B1:** Backup a volume using `docker run --rm -v notes-data:/data -v $(pwd):/backup alpine tar czf /backup/notes-backup.tar.gz /data`.
- **B2:** Use `--mount` syntax instead of `-v` (it's more verbose but more explicit). Look up the syntax.
- **B3:** Try using `tmpfs` mount (in-memory, not persistent). Use `--tmpfs /tmp` in docker run.
