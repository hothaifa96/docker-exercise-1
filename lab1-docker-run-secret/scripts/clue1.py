#!/usr/bin/env python3
"""
CLUE 1 — Python Docker Trivia
Answer all 3 questions correctly to earn Clue 1.
Run with: python3 /scripts/clue1.py
"""

import sys

CLUE = "DOCKER"

questions = [
    {
        "q":      "Q1: What Docker command lists ALL running containers?",
        "hint":   "It shows a table of containers — like 'ps' in Linux.",
        "answers": ["docker ps", "ps"]
    },
    {
        "q":      "Q2: What flag do you pass to 'docker run' to remove the container automatically when it exits?",
        "hint":   "It's two dashes followed by two letters.",
        "answers": ["--rm"]
    },
    {
        "q":      "Q3: What command executes a shell command inside an ALREADY RUNNING container?",
        "hint":   "docker ___ -it <container> bash",
        "answers": ["docker exec", "exec"]
    }
]

print()
print("=" * 50)
print("  🐍 PYTHON DOCKER TRIVIA — GET CLUE 1")
print("=" * 50)
print("  Answer all 3 questions correctly for Clue 1.")
print("=" * 50)
print()

score = 0

for i, q in enumerate(questions, 1):
    print(q["q"])
    try:
        answer = input("  Your answer: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Interrupted. Try again: python3 /scripts/clue1.py")
        sys.exit(1)

    correct = any(a.lower() in answer for a in q["answers"])
    if correct:
        print("  ✅  Correct!\n")
        score += 1
    else:
        print(f"  ❌  Wrong!  Hint: {q['hint']}\n")

print("-" * 50)
if score == len(questions):
    print(f"  🎉  Perfect score ({score}/{len(questions)})!")
    print()
    print(f"  ┌─────────────────────────────┐")
    print(f"  │  CLUE 1  →  [ {CLUE:<14} ]│")
    print(f"  └─────────────────────────────┘")
    print()
    print("  Now get Clue 2 by running:")
    print("  → node /scripts/trivia.js")
else:
    print(f"  😬  You got {score}/{len(questions)}. You need ALL 3 correct!")
    print("  Try again: python3 /scripts/clue1.py")
    print()
    print("  💡 Stuck? Check /hints/hint.txt for a nudge.")
print()
