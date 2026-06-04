/**
 * Lab 4 — Frontend JavaScript
 *
 * The browser talks to the backend via the EXPOSED HOST PORT (localhost:5000).
 * Container DNS (backend → backend) is a server-side concept — the browser
 * always talks to exposed ports on the host machine.
 *
 * Change BACKEND_URL if your backend runs on a different port.
 */

const BACKEND_URL = "http://localhost:5000";

async function apiFetch(path, options = {}) {
  const res = await fetch(BACKEND_URL + path, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

function showError(msg) {
  const el = document.getElementById("error-msg");
  el.textContent = "⚠️ " + msg;
  el.style.display = "block";
  setTimeout(() => { el.style.display = "none"; }, 5000);
}

async function loadTasks() {
  try {
    const data = await apiFetch("/api/tasks");
    renderTasks(data.tasks);
    document.getElementById("server-info").textContent =
      `Container: ${data.server} | Tasks stored in-memory (add a volume in Lab 3 to persist!)`;
    document.getElementById("error-msg").style.display = "none";
    await loadStats();
  } catch (e) {
    showError("Could not connect to backend at " + BACKEND_URL +
      " — is the backend container running with -p 5000:5000?");
    document.getElementById("server-info").textContent = "Backend unreachable";
  }
}

async function loadStats() {
  try {
    const s = await apiFetch("/api/stats");
    document.getElementById("stat-total").textContent   = s.total;
    document.getElementById("stat-pending").textContent = s.pending;
    document.getElementById("stat-done").textContent    = s.completed;
  } catch (_) {}
}

function renderTasks(tasks) {
  const list = document.getElementById("task-list");
  if (tasks.length === 0) {
    list.innerHTML = '<li style="text-align:center;color:#8b949e;padding:20px">No tasks yet. Add one above!</li>';
    return;
  }
  list.innerHTML = tasks.map(t => `
    <li class="task-item ${t.completed ? "done" : ""}" id="task-${t.id}">
      <span class="task-title">${escapeHtml(t.title)}</span>
      <span class="priority ${t.priority}">${t.priority}</span>
      <div class="task-actions">
        <button class="btn-done" onclick="toggleTask(${t.id}, ${!t.completed})">
          ${t.completed ? "↩ Undo" : "✓ Done"}
        </button>
        <button class="btn-danger" onclick="deleteTask(${t.id})">✕</button>
      </div>
    </li>
  `).join("");
}

async function addTask() {
  const input    = document.getElementById("task-input");
  const priority = document.getElementById("priority-input").value;
  const title    = input.value.trim();
  if (!title) return;

  try {
    await apiFetch("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title, priority })
    });
    input.value = "";
    await loadTasks();
  } catch (e) {
    showError("Failed to add task: " + e.message);
  }
}

async function toggleTask(id, completed) {
  try {
    await apiFetch(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify({ completed })
    });
    await loadTasks();
  } catch (e) {
    showError("Failed to update task: " + e.message);
  }
}

async function deleteTask(id) {
  try {
    await apiFetch(`/api/tasks/${id}`, { method: "DELETE" });
    await loadTasks();
  } catch (e) {
    showError("Failed to delete task: " + e.message);
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

document.getElementById("task-input").addEventListener("keypress", e => {
  if (e.key === "Enter") addTask();
});

loadTasks();
setInterval(loadTasks, 5000);
