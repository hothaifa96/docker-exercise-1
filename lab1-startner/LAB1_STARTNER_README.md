# Lab 1-Startner — Docker Run & The Secret Hunt

> **Goal:** Discover the secret word hidden inside the container.
> It is split into **two clues**. You need BOTH to assemble the secret word.

---

## Step 1 — Build & start the hunt container

```bash
# Build the image locally
docker build -t startner-hunt .

# Run it in detached mode
docker run --rm -d --name hunt startner-hunt

# Confirm it is running
docker ps
```

---

## Step 2 — Enter the container

```bash
docker exec -it hunt bash
```

Look around — what files are inside?

```bash
ls /scripts
ls /hints
```

---

## Step 3.1 — Get CLUE 1 (Python Trivia)

```bash
# Inside the container:
python3 /scripts/clue1.py
```

Answer all **3 Docker trivia questions** correctly to reveal **CLUE 1**.

> ⚠️ You need a **perfect score (3/3)** to get the clue!

---

## Step 3.2 — Get CLUE 2 (JavaScript Trivia)

```bash
# Still inside the container:
node /scripts/trivia.js
```

Answer all 3 JavaScript trivia questions about Docker to get **CLUE 2**.

> ⚠️ You need a **perfect score (3/3)** to get the clue!

---

## Step 3.3 — Reveal the secret word

Once you have both clues, combine them to form the secret word.
Then confirm by running:

```bash
# Still inside the container:
cat /hints/secret.txt
```

> 🎉 You found the secret word!

---

## Cleanup

```bash
# Exit the container first (type: exit), then:
docker stop hunt
docker rmi startner-hunt
```
