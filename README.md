# Lab 1 — Docker Run & The 
> **Goal:** Discover the secret word hidden inside the container.  
> It is split into **two clues**. You need BOTH to assemble the secret word.

### Step 3.1 — Start the hunt container in detached mode

```bash
docker run --rm -d --name hunt hothaifaz11/try-me

# Confirm it is running
docker ps
```

### Step 3.2 — Enter the container

```bash
docker exec -it ....

# Look around — what files are inside?

### Step 3.3 — Get CLUE 1 (Python Challenge)

run it ?

Answer the 3 Docker trivia questions correctly to reveal **CLUE 1**.

> ⚠️ You need a **perfect score (3/3)** to get the clue!

### Step 3.4 — Get CLUE 2 (JavaScript Trivia)

```bash
# Still inside the container:
node ....
```

Answer all 3 JavaScript trivia questions about Docker correctly to get **CLUE 2**.

### Step 3.5 — Reveal the secret word

Once you have both clues, combine them to form the secret word.  
Then confirm by running:

```bash
# Still inside the container:
/hints/secret.txt
```

> 🎉 You found the secret word!
