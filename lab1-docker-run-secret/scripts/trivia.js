#!/usr/bin/env node
/**
 * CLUE 2 — JavaScript Docker Trivia
 * Answer all 3 questions correctly to earn Clue 2.
 * Run with: node /scripts/trivia.js
 */

const readline = require("readline");

const CLUE = "_NINJA";

const questions = [
  {
    q: "Q1: What special file tells Docker HOW to build an image?\n   (It lives in your project folder and starts with a capital D)",
    answers: ["dockerfile"],
    hint:    "It's named: Dockerfile"
  },
  {
    q: "Q2: What Dockerfile keyword sets the BASE IMAGE for your container?",
    answers: ["from"],
    hint:    "It's the very FIRST instruction in every Dockerfile — FROM"
  },
  {
    q: "Q3: What Docker command shows the LIVE logs output of a running container?",
    answers: ["docker logs", "logs"],
    hint:    "docker ___ <container_name>"
  }
];

const rl = readline.createInterface({
  input:  process.stdin,
  output: process.stdout
});

let index = 0;
let score = 0;

console.log();
console.log("=".repeat(50));
console.log("  🟨 JS DOCKER TRIVIA — GET CLUE 2");
console.log("=".repeat(50));
console.log("  Answer all 3 questions correctly for Clue 2.");
console.log("=".repeat(50));
console.log();

function ask() {
  if (index >= questions.length) {
    console.log("-".repeat(50));
    if (score === questions.length) {
      console.log(`  🎉  Outstanding! Perfect score (${score}/${questions.length})!`);
      console.log();
      console.log(`  ┌─────────────────────────────┐`);
      console.log(`  │  CLUE 2  →  [ ${CLUE.padEnd(14)} ]│`);
      console.log(`  └─────────────────────────────┘`);
      console.log();
      console.log("  🔐  Now combine BOTH clues to reveal the secret word.");
      console.log("  💡  CLUE 1  +  CLUE 2  =  ???");
      console.log();
      console.log("  Verify your answer: cat /hints/secret.txt");
    } else {
      console.log(`  😬  You got ${score}/${questions.length}. You need ALL 3 correct!`);
      console.log("  Try again: node /scripts/trivia.js");
    }
    console.log();
    rl.close();
    return;
  }

  const q = questions[index];
  console.log(`  ${q.q}`);
  rl.question("  Your answer: ", (ans) => {
    const clean = ans.trim().toLowerCase();
    const correct = q.answers.some(a => clean.includes(a));
    if (correct) {
      console.log("  ✅  Correct!\n");
      score++;
    } else {
      console.log(`  ❌  Wrong!  Hint: ${q.hint}\n`);
    }
    index++;
    ask();
  });
}

ask();
