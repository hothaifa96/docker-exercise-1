/**
 * Lab 3 — Frontend
 * Fetches log files from the backend API and renders them.
 * The backend URL is configurable via the BACKEND_URL global
 * (set by nginx or defaults to localhost:4000 for development).
 */

const API = (typeof BACKEND_URL !== 'undefined' ? BACKEND_URL : 'http://localhost:4000');

let currentFile      = null;
let autoRefreshTimer = null;

/* ── DOM refs ── */
const fileList      = document.getElementById('file-list');
const fileCount     = document.getElementById('file-count');
const logOutput     = document.getElementById('log-output');
const openFileName  = document.getElementById('open-file-name');
const lineCount     = document.getElementById('line-count');
const refreshBtn    = document.getElementById('refresh-btn');
const autoRefresh   = document.getElementById('auto-refresh');

/* ── Fetch file list ── */
async function loadFiles() {
  try {
    const res  = await fetch(`${API}/files`);
    const data = await res.json();
    renderFileList(data.files || []);
  } catch (err) {
    fileList.innerHTML = `<div style="padding:16px;color:#f87171;font-size:12px;">
      ⚠ Cannot reach backend at <code>${API}</code><br/>
      Is the backend container running?</div>`;
  }
}

/* ── Render sidebar file list ── */
function renderFileList(files) {
  if (files.length === 0) {
    fileList.innerHTML = `<div style="padding:20px 16px;color:#4b5563;font-size:12px;text-align:center;">
      No .log files yet.<br/>Wait for the worker to generate some.</div>`;
    fileCount.textContent = '';
    return;
  }

  fileList.innerHTML = files.map(f => `
    <div class="file-item ${f === currentFile ? 'active' : ''}" data-file="${f}">
      <span class="icon">📄</span>
      <span>${f}</span>
    </div>
  `).join('');

  fileCount.textContent = `${files.length} file${files.length !== 1 ? 's' : ''}`;

  fileList.querySelectorAll('.file-item').forEach(el => {
    el.addEventListener('click', () => openFile(el.dataset.file));
  });
}

/* ── Open and render a log file ── */
async function openFile(filename) {
  currentFile = filename;

  document.querySelectorAll('.file-item').forEach(el => {
    el.classList.toggle('active', el.dataset.file === filename);
  });

  openFileName.textContent = filename;
  openFileName.style.color = '#e0e0e0';
  logOutput.innerHTML = `<div style="color:#4b5563;padding:20px;font-size:12px;">Loading…</div>`;

  try {
    const res  = await fetch(`${API}/files/${filename}`);
    const data = await res.json();

    if (data.error) {
      logOutput.innerHTML = `<div style="color:#f87171;padding:20px;">${data.error}</div>`;
      return;
    }

    renderLines(data.lines || []);
    lineCount.textContent = `${data.total} lines`;
    scrollToBottom();
  } catch (err) {
    logOutput.innerHTML = `<div style="color:#f87171;padding:20px;">Failed to load file.</div>`;
  }
}

/* ── Render log lines with colour coding ── */
function renderLines(lines) {
  if (lines.length === 0) {
    logOutput.innerHTML = `<div class="placeholder"><div>File is empty — wait for the worker.</div></div>`;
    return;
  }

  const html = lines.map((line, i) => {
    const level    = detectLevel(line);
    const htmlLine = highlightLine(escapeHtml(line));
    return `<div class="log-line log-${level.toLowerCase()}">
      <span class="ln">${i + 1}</span>
      <span class="text">${htmlLine}</span>
    </div>`;
  }).join('');

  logOutput.innerHTML = html;
}

function detectLevel(line) {
  if (line.includes('[ERROR]')) return 'ERROR';
  if (line.includes('[WARN')) return 'WARN';
  return 'INFO';
}

function highlightLine(line) {
  return line
    .replace(/\[INFO\s*\]/g,  '<span class="tag-INFO">[INFO ]</span>')
    .replace(/\[WARN\s*\]/g,  '<span class="tag-WARN">[WARN ]</span>')
    .replace(/\[ERROR\]/g, '<span class="tag-ERROR">[ERROR]</span>');
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function scrollToBottom() {
  logOutput.scrollTop = logOutput.scrollHeight;
}

/* ── Auto-refresh ── */
function startAutoRefresh() {
  if (autoRefreshTimer) clearInterval(autoRefreshTimer);
  autoRefreshTimer = setInterval(async () => {
    await loadFiles();
    if (currentFile) await openFile(currentFile);
  }, 4000);
}

function stopAutoRefresh() {
  if (autoRefreshTimer) clearInterval(autoRefreshTimer);
  autoRefreshTimer = null;
}

autoRefresh.addEventListener('change', () => {
  autoRefresh.checked ? startAutoRefresh() : stopAutoRefresh();
});

refreshBtn.addEventListener('click', async () => {
  refreshBtn.textContent = '↻';
  await loadFiles();
  if (currentFile) await openFile(currentFile);
  setTimeout(() => { refreshBtn.textContent = '⟳'; }, 500);
});

/* ── Boot ── */
loadFiles();
startAutoRefresh();
