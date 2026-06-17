const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 5000;

// In-memory storage for todos
let todos = [
  { id: 1, text: 'Learn Docker', completed: false },
  { id: 2, text: 'Build React app', completed: false },
  { id: 3, text: 'Deploy to production', completed: false }
];

app.use(cors());
app.use(express.json());

// Get all todos
app.get('/api/todos', (req, res) => {
  res.json(todos);
});

// Get a single todo
app.get('/api/todos/:id', (req, res) => {
  const todo = todos.find(t => t.id === parseInt(req.params.id));
  if (!todo) return res.status(404).json({ error: 'Todo not found' });
  res.json(todo);
});

// Create a new todo
app.post('/api/todos', (req, res) => {
  const { text } = req.body;
  if (!text) return res.status(400).json({ error: 'Text is required' });
  
  const newTodo = {
    id: todos.length > 0 ? Math.max(...todos.map(t => t.id)) + 1 : 1,
    text,
    completed: false
  };
  
  todos.push(newTodo);
  res.status(201).json(newTodo);
});

// Update a todo
app.put('/api/todos/:id', (req, res) => {
  const todo = todos.find(t => t.id === parseInt(req.params.id));
  if (!todo) return res.status(404).json({ error: 'Todo not found' });
  
  const { text, completed } = req.body;
  if (text !== undefined) todo.text = text;
  if (completed !== undefined) todo.completed = completed;
  
  res.json(todo);
});

// Delete a todo
app.delete('/api/todos/:id', (req, res) => {
  const index = todos.findIndex(t => t.id === parseInt(req.params.id));
  if (index === -1) return res.status(404).json({ error: 'Todo not found' });
  
  todos.splice(index, 1);
  res.status(204).send();
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
  console.log(`Todo backend running on port ${PORT}`);
  console.log(`API available at http://localhost:${PORT}/api/todos`);
});
