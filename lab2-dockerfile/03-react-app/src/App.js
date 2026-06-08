import React, { useState, useEffect } from 'react';

const cardStyle = {
  fontFamily: 'system-ui, sans-serif',
  maxWidth: 520,
  margin: '80px auto',
  padding: '40px',
  borderRadius: 12,
  boxShadow: '0 4px 24px rgba(0,0,0,0.12)',
  textAlign: 'center',
  background: '#fff'
};

const badgeStyle = {
  display: 'inline-block',
  background: '#0db7ed',
  color: '#fff',
  borderRadius: 6,
  padding: '4px 14px',
  fontSize: 13,
  marginBottom: 24,
  fontWeight: 600,
  letterSpacing: 1
};

export default function App() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div style={cardStyle}>
      <div style={badgeStyle}>🐳 RUNNING IN DOCKER</div>
      <h1 style={{ fontSize: 28, margin: '0 0 8px' }}>Hello from React!</h1>
      <p style={{ color: '#555', marginBottom: 24 }}>
        This React app was built inside Docker using a <strong>multi-stage Dockerfile</strong>
        {' '}and is now served by <strong>nginx</strong>.
      </p>
      <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '16px', fontSize: 14, color: '#333' }}>
        <strong>Container time:</strong> {time}
      </div>
    </div>
  );
}
