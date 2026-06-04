# ⚙️ Lab 5 — Environment Variables

## 🎯 Concept
Containers should be **configurable without changing code or rebuilding images**.  
Environment variables are the standard way to pass configuration to containers.  
This is a core principle of the **12-Factor App** methodology.

---

## 📋 Ways to Set Environment Variables

| Method | How | When to use |
|--------|-----|------------|
| `ENV` in Dockerfile | Baked into the image | Defaults / non-sensitive |
| `docker run -e` | Single variable at runtime | Quick overrides |
| `docker run --env-file` | Load from a file | Many variables |
| `docker-compose.yml` | `environment:` section | Compose setups |
| Secrets manager | Vault, AWS SSM, etc. | Sensitive data in production |

> ⚠️ **Never hardcode secrets** (API keys, passwords) in Dockerfiles or source code!

---

## 🐍 The App — Configurable Flask Dashboard

This Flask app reads all its configuration from environment variables.  
Change the env vars → change the app's behavior — no code changes needed.

### Configurable Variables

| Variable | Default | Effect |
|----------|---------|--------|
| `APP_NAME` | `Docker Config App` | App title shown in UI |
| `ENVIRONMENT` | `production` | Changes app theme & debug mode |
| `SECRET_KEY` | `changeme-insecure` | Flask secret (sign cookies) |
| `DATABASE_URL` | `sqlite:///app.db` | Simulated DB connection string |
| `MAX_ITEMS` | `100` | Business logic parameter |
| `FEATURE_DARK_MODE` | `false` | Feature flag |
| `ADMIN_EMAIL` | `admin@example.com` | Contact shown in footer |
| `PORT` | `5000` | Port the app listens on |

---

## 🚀 PART 1 — ENV in Dockerfile (Baked-in Defaults)

```bash
cd lab5-env-variables

# Build the image
docker build -t config-app:v1 .

# Run with ALL defaults from Dockerfile
docker run -d --name app-defaults -p 5000:5000 config-app:v1

# Visit http://localhost:5000
# The app runs with default ENV values from the Dockerfile

# Inspect what env vars are set
docker exec app-defaults env

docker stop app-defaults && docker rm app-defaults
```

---

## 🚀 PART 2 — Override with -e Flag

```bash
# Override individual environment variables at runtime
docker run -d --name app-dev \
  -p 5000:5000 \
  -e APP_NAME="My Dev App" \
  -e ENVIRONMENT=development \
  -e FEATURE_DARK_MODE=true \
  -e MAX_ITEMS=50 \
  config-app:v1

# Visit http://localhost:5000
# Notice the app title, theme, and settings have changed!

# Print just specific env vars
docker exec app-dev printenv APP_NAME
docker exec app-dev printenv ENVIRONMENT
docker exec app-dev env | grep -E "APP_|ENVIRONMENT|FEATURE_"

docker stop app-dev && docker rm app-dev
```

---

## 🚀 PART 3 — Load from --env-file

```bash
# Create an env file (copy from the example)
cp .env.example .env

# Edit .env to your preferences (open it in a text editor)
# Then run with --env-file
docker run -d --name app-envfile \
  -p 5000:5000 \
  --env-file .env \
  config-app:v1

# Visit http://localhost:5000 — all settings from .env are applied

docker stop app-envfile && docker rm app-envfile
```

> 💡 **Security tip:** Never commit `.env` files to git! Add `.env` to your `.gitignore`.

---

## 🚀 PART 4 — Production vs Development

```bash
# Run as PRODUCTION (secure, minimal info exposure)
docker run -d --name app-prod \
  -p 5000:5000 \
  -e ENVIRONMENT=production \
  -e APP_NAME="Prod App" \
  -e SECRET_KEY="super-secret-prod-key-never-share" \
  config-app:v1

# Run as DEVELOPMENT (verbose, debug info shown)
docker run -d --name app-dev \
  -p 5001:5000 \
  -e ENVIRONMENT=development \
  -e APP_NAME="Dev App" \
  -e SECRET_KEY="dev-only-key" \
  config-app:v1

# Compare the two UIs side by side:
# http://localhost:5000  →  production (dark, restricted info)
# http://localhost:5001  →  development (shows more debug info)

docker stop app-prod app-dev
docker rm app-prod app-dev
```

---

## 🚀 PART 5 — Inspect Variables from Inside the Container

```bash
docker run -d --name app-inspect \
  -e MY_SECRET="top-secret-value" \
  -e DATABASE_URL="postgres://user:pass@db:5432/mydb" \
  config-app:v1

# See ALL environment variables inside the container
docker exec app-inspect env

# Get a specific variable
docker exec app-inspect printenv MY_SECRET

# From the host, inspect env via docker inspect
docker inspect app-inspect | grep -A 30 '"Env"'

docker stop app-inspect && docker rm app-inspect
```

> ⚠️ `docker inspect` shows env vars in **plain text** — avoid secrets in env vars
> in production. Use Docker Secrets or a secrets manager instead.

---

## 🚀 PART 6 — ARG vs ENV (Build Time vs Runtime)

```bash
# ARG is available ONLY at build time
# ENV is available at both build time AND runtime

# Build with a custom ARG
docker build --build-arg APP_VERSION=2.5 -t config-app:v2.5 .

# Verify the version is baked in
docker run --rm config-app:v2.5 printenv APP_VERSION

# Try to override APP_VERSION at runtime
docker run --rm -e APP_VERSION=3.0 config-app:v2.5 printenv APP_VERSION
# Still 2.5 — ARG is set at build time, but ENV persists at runtime
```

---

## 🧹 Cleanup

```bash
docker stop $(docker ps -q --filter name=app-)
docker rm $(docker ps -aq --filter name=app-)
```

---

## 🎓 Exercises

1. Build the image and run it with NO env overrides. Visit `/config` — what defaults are shown?
2. Override `ENVIRONMENT=development` and `FEATURE_DARK_MODE=true` using `-e`. What changes?
3. Create your own `.env` file from `.env.example`. Add `CUSTOM_MESSAGE="Hello class!"`. Run with `--env-file` and see it in `/config`.
4. Run the same image with `ENVIRONMENT=production` and `ENVIRONMENT=development` on different ports. Compare the outputs at `GET /config`.
5. Use `docker inspect` to read the env vars of a running container from the host.

---

## 🏆 Bonus Challenges

- **B1:** Research **Docker Secrets** (`docker secret create`). How are they safer than env vars?
- **B2:** Add a `GET /greet` endpoint that reads a `GREETING_LANG` env var and returns "Hello" in different languages.
- **B3:** Build the image once and run it as **dev**, **staging**, and **production** simultaneously on ports 5000, 5001, 5002 — each with different `APP_NAME` and `ENVIRONMENT` values.
