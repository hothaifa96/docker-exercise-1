const express = require('express');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'demo',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres'
});

app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Backend is running' });
});

// Get all messages from database
app.get('/api/messages', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM messages ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('Error fetching messages:', err);
    res.status(500).json({ error: 'Failed to fetch messages' });
  }
});

// Add a new message
app.post('/api/messages', async (req, res) => {
  const { text, author } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO messages (text, author) VALUES ($1, $2) RETURNING *',
      [text, author]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error adding message:', err);
    res.status(500).json({ error: 'Failed to add message' });
  }
});

// Initialize database table
app.post('/api/init', async (req, res) => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    res.json({ message: 'Database initialized successfully' });
  } catch (err) {
    console.error('Error initializing database:', err);
    res.status(500).json({ error: 'Failed to initialize database' });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});
