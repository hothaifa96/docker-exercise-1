# 🏗 Lab 2 — Building Docker Images (Multi-Language)

## 🎯 Concept
Write `Dockerfile`s for real applications in three languages.  
Understand every instruction — what it does, why it's there, and how layers work.

---

## 📋 Dockerfile Instructions Reference

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Set the base image (always first) |
| `LABEL` | Add metadata (maintainer, version, etc.) |
| `WORKDIR` | Set working directory inside image |
| `COPY` | Copy files from host → image |
| `ADD` | Like COPY but can unpack archives and fetch URLs |
| `RUN` | Execute a command during BUILD (creates a layer) |
| `ENV` | Set environment variables |
| `EXPOSE` | Document which port the app listens on |
| `CMD` | Default command when container starts (overridable) |
| `ENTRYPOINT` | Fixed command (CMD becomes its arguments) |
| `ARG` | Build-time variable (not available at runtime) |
| `.dockerignore` | Files/folders to EXCLUDE from the build context |

---

## 🐍 APP 1 — Python Flask Web App

### What the app does
A simple Flask API that returns:
- `GET /` → Hello message with container info
- `GET /info` → JSON with Python version, hostname, environment
- `GET /health` → Health check endpoint

### Dockerfile steps explained

**Step 1 — FROM**  
We choose `python:3.11-slim` (smaller than `python:3.11`, has no dev tools).

**Step 2 — WORKDIR**  
Sets `/app` as working directory. All subsequent commands run from here.

**Step 3 — COPY requirements.txt first**  
Copying requirements.txt BEFORE the source code is a key optimization.  
Docker caches each layer — if requirements.txt didn't change, it reuses  
the pip install layer even when your code changes.

**Step 4 — RUN pip install**  
Installs dependencies into the image during build time.

**Step 5 — COPY . .**  
Copy the rest of the source code into the image.

**Step 6 — EXPOSE**  
Documents port 5000 (Flask default). Does NOT actually open the port.

**Step 7 — CMD**  
Defines the default command. We use the JSON array form (preferred).

### Build and run

```bash
cd lab2-basic-images/python-flask

# Build the image
docker build -t flask-app:v1 .

# See the layers created
docker history flask-app:v1

# Run it
docker run -d --name flask-demo -p 5000:5000 flask-app:v1

# Test it
curl http://localhost:5000/
curl http://localhost:5000/info
curl http://localhost:5000/health

# View logs
docker logs flask-demo

# Stop and remove
docker stop flask-demo && docker rm flask-demo
```

### Layer caching experiment

```bash
# Build again — notice it reuses ALL layers (very fast)
docker build -t flask-app:v1 .

# Now modify app.py (change the greeting text)
# Build again — only the COPY . . layer and after are re-executed
docker build -t flask-app:v1 .
```

---

## ☕ APP 2 — Java HTTP Server

### What the app does
A Java app using the built-in `com.sun.net.httpserver` package.  
- `GET /` → Hello from Java + JVM info
- `GET /health` → JSON health check

### Dockerfile steps explained

**Step 1 — Multi-stage build**  
Stage 1 (`builder`): Uses `openjdk:17-slim` to compile `.java` → `.class` files.  
Stage 2 (`runtime`): Uses `openjdk:17-jre-slim` (smaller, no compiler) to run.  
The final image does NOT contain the source code or compiler!

**Step 2 — COPY, RUN javac**  
Compile the Java source in the builder stage.

**Step 3 — COPY --from=builder**  
Copy only the compiled `.class` file into the runtime image.

**Step 4 — CMD**  
Run the compiled class.

### Build and run

```bash
cd lab2-basic-images/java-app

docker build -t java-app:v1 .
docker run -d --name java-demo -p 8080:8080 java-app:v1

curl http://localhost:8080/
curl http://localhost:8080/health

docker stop java-demo && docker rm java-demo
```

### Notice the size difference

```bash
# Compare image sizes
docker images | grep -E "flask-app|java-app"
```

---

## 💙 APP 3 — C# ASP.NET Core API

### What the app does
A minimal .NET 8 Web API:
- `GET /` → Hello from C# + machine info
- `GET /info` → OS, runtime, container details
- `GET /health` → Health check

### Dockerfile steps explained

**Step 1 — Multi-stage build**  
Stage 1 (`build`): `mcr.microsoft.com/dotnet/sdk:8.0` — full SDK to compile.  
Stage 2 (`runtime`): `mcr.microsoft.com/dotnet/aspnet:8.0` — lightweight runtime only.  
This is essential — the SDK image is ~700 MB, the runtime is ~200 MB!

**Step 2 — COPY .csproj, RUN dotnet restore**  
Restore NuGet packages first (layer caching optimization — same as pip).

**Step 3 — COPY . ., RUN dotnet publish**  
Publish the release build (compiled DLLs) to `/app/publish`.

**Step 4 — COPY --from=build**  
Bring only the published output into the runtime image.

**Step 5 — ENTRYPOINT**  
Use ENTRYPOINT (not CMD) because dotnet is always the executable.

### Build and run

```bash
cd lab2-basic-images/csharp-app

docker build -t csharp-app:v1 .
docker run -d --name csharp-demo -p 7000:8080 csharp-app:v1

curl http://localhost:7000/
curl http://localhost:7000/info
curl http://localhost:7000/health

docker stop csharp-demo && docker rm csharp-demo
```

---

## 🏷 Tagging and Pushing Images

```bash
# Tag with version
docker tag flask-app:v1 flask-app:latest
docker tag flask-app:v1 myusername/flask-app:v1

# Push to Docker Hub (requires: docker login)
docker login
docker push myusername/flask-app:v1

# Pull it back from any machine
docker pull myusername/flask-app:v1
```

---

## 🎓 Exercises

1. **Edit** `python-flask/app.py` and add a `GET /time` endpoint that returns the current UTC time. Rebuild the image — which layers were cached?
2. **Inspect** the size of all three images: `docker images`. Which is biggest? Why?
3. **Add** an `ARG APP_VERSION=1.0` to the Python Dockerfile and print it in the `/info` endpoint.
4. **Create** a `.dockerignore` file in `python-flask/` to exclude `__pycache__` and `.pyc` files from the build context.
5. **Experiment** with `ENTRYPOINT` vs `CMD`: Change the Python Dockerfile to use `ENTRYPOINT ["python3"]` and `CMD ["app.py"]`. What happens if you run `docker run flask-app:v1 --version`?

---

## 🏆 Bonus Challenges

- **B1:** Build the Python image and use `dive` tool (install separately) to explore the layers.
- **B2:** Write a `Dockerfile` for a **JavaScript (Node.js + Express)** app that serves `Hello from Node!`.
- **B3:** Try building the Python image with `python:3.11` (full) vs `python:3.11-slim` vs `python:3.11-alpine`. Compare sizes.
- **B4:** Add a `HEALTHCHECK` instruction to the Python Dockerfile that pings `/health` every 30 seconds.
