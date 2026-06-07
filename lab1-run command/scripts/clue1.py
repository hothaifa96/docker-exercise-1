#!/usr/bin/env python3
"""
CLUE 1 — Python Docker Trivia
Answer all 3 questions correctly to earn Clue 1.
Run with: python3 /scripts/clue1.py
"""

import sys

CLUE = "PULL"

questions = [
    {
        "q":      "Q1: What Docker command downloads an image from Docker Hub WITHOUT running it?",
        "hint":   "docker ___  ubuntu:22.04  (just downloads, does not start anything)",
        "answers": ["docker pull", "pull"]
    },
    {
        "q":      "Q2: What flag do you add to 'docker run' to start the container in the BACKGROUND (detached)?",
        "hint":   "It is a single dash followed by a single letter: -_",
        "answers": ["-d"]
    },
    {
        "q":      "Q3: What command shows the LIVE output (logs) of a running container?",
        "hint":   "docker ___ <container_name>",
        "answers": ["docker logs", "logs"]
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
