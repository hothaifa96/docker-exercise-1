/**
 * Lab 3 — Backend Service
 * Reads log files from the shared Docker volume (/logs)
 * and exposes them via a simple REST API.
 *
 * GET  /files            → list all .log files
 * GET  /files/:filename  → return content of one file
 * GET  /health           → health check
 */

const express = require('express');
const cors    = require('cors');
const fs      = require('fs');
const path    = require('path');

const app     = express();
const PORT    = process.env.PORT    || 4000;
const LOG_DIR = process.env.LOG_DIR || '/logs';

app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', log_dir: LOG_DIR });
});

app.get('/files', (_req, res) => {
  fs.readdir(LOG_DIR, (err, files) => {
    if (err) {
      console.error('[backend] Cannot read log dir:', err.message);
      return res.status(500).json({ error: 'Cannot read log directory' });
    }
    const logFiles = files
      .filter(f => f.endsWith('.log'))
      .sort()
      .reverse();
    res.json({ files: logFiles, count: logFiles.length });
  });
});

app.get('/files/:filename', (req, res) => {
  const { filename } = req.params;

  if (filename.includes('..') || filename.includes('/')) {
    return res.status(400).json({ error: 'Invalid filename' });
  }

  const filePath = path.join(LOG_DIR, filename);

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(404).json({ error: `File not found: ${filename}` });
    }

    const lines = data.trim().split('\n').filter(Boolean);
    res.json({ filename, lines, total: lines.length });
  });
});

app.listen(PORT, () => {
  console.log(`[backend] API running on http://localhost:${PORT}`);
  console.log(`[backend] Watching log directory: ${LOG_DIR}`);
});
