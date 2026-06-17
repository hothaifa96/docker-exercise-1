import React, { useState, useEffect } from 'react';

const API_URL =
  process.env.REACT_APP_API_URL || "http://localhost:4040/api/todos";

function App() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
      });
      const newTodo = await response.json();
      setTodos([...todos, newTodo]);
      setInput('');
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const toggleTodo = async (id) => {
    const todo = todos.find(t => t.id === id);
    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed })
      });
      const updatedTodo = await response.json();
      setTodos(todos.map(t => t.id === id ? updatedTodo : t));
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      setTodos(todos.filter(t => t.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>Todo App</h1>
      <form onSubmit={addTodo} style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Add a new todo..."
          style={{
            flex: 1,
            padding: 10,
            fontSize: 16,
            border: '1px solid #ddd',
            borderRadius: 4
          }}
        />
        <button
          type="submit"
          style={{
            padding: '10 20',
            fontSize: 16,
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer'
          }}
        >
          Add
        </button>
      </form>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map(todo => (
          <li key={todo.id} style={{
            display: 'flex',
            alignItems: 'center',
            padding: 10,
            marginBottom: 8,
            backgroundColor: '#f9f9f9',
            borderRadius: 4,
            border: '1px solid #eee'
          }}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
              style={{ marginRight: 10, cursor: 'pointer' }}
            />
            <span style={{
              flex: 1,
              textDecoration: todo.completed ? 'line-through' : 'none',
              color: todo.completed ? '#999' : '#333'
            }}>
              {todo.text}
            </span>
            <button
              onClick={() => deleteTodo(todo.id)}
              style={{
                padding: '5 10',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: 4,
                cursor: 'pointer'
              }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      {todos.length === 0 && (
        <p style={{ textAlign: 'center', color: '#999' }}>No todos yet. Add one above!</p>
      )}
    </div>
  );
}

export default App;
