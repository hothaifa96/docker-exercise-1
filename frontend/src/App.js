import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [games, setGames] = useState([]);
  const [currentGame, setCurrentGame] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchGames = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/games`);
      setGames(response.data);
    } catch (err) {
      setError('Failed to fetch games');
    }
  };

  useEffect(() => {
    fetchGames();
    const interval = setInterval(fetchGames, 2000);
    return () => clearInterval(interval);
  }, []);

  const createGame = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/games`);
      setCurrentGame(response.data);
      fetchGames();
    } catch (err) {
      setError('Failed to create game');
    }
    setLoading(false);
  };

  const loadGame = async (gameId) => {
    try {
      const response = await axios.get(`${API_URL}/api/games/${gameId}`);
      setCurrentGame(response.data);
    } catch (err) {
      setError('Failed to load game');
    }
  };

  const makeMove = async (position) => {
    if (!currentGame || currentGame.status !== 'ongoing') return;
    
    try {
      const response = await axios.post(`${API_URL}/api/games/${currentGame.id}/move`, {
        position
      });
      setCurrentGame(response.data);
      fetchGames();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to make move');
      setTimeout(() => setError(null), 3000);
    }
  };

  const deleteGame = async (gameId) => {
    try {
      await axios.delete(`${API_URL}/api/games/${gameId}`);
      if (currentGame?.id === gameId) setCurrentGame(null);
      fetchGames();
    } catch (err) {
      setError('Failed to delete game');
    }
  };

  const renderCell = (index) => {
    const cell = currentGame?.board?.[index] || ' ';
    return (
      <button
        key={index}
        className={`cell ${cell !== ' ' ? 'filled' : ''} ${cell === 'X' ? 'x-mark' : 'o-mark'}`}
        onClick={() => makeMove(index)}
        disabled={cell !== ' ' || currentGame?.status !== 'ongoing'}
      >
        {cell !== ' ' ? cell : ''}
      </button>
    );
  };

  const getStatusMessage = () => {
    if (!currentGame) return 'Create or select a game to start';
    if (currentGame.status === 'finished') {
      if (currentGame.winner) return `Player ${currentGame.winner} wins! 🎉`;
      return "It's a draw! 🤝";
    }
    return `Current player: ${currentGame.current_player}`;
  };

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">XO Game</h1>
        
        <div className="game-layout">
          <div className="sidebar">
            <button className="btn btn-primary" onClick={createGame} disabled={loading}>
              {loading ? 'Creating...' : 'New Game'}
            </button>
            
            <div className="games-list">
              <h3>Active Games</h3>
              {games.map(game => (
                <div 
                  key={game.id} 
                  className={`game-item ${currentGame?.id === game.id ? 'active' : ''}`}
                >
                  <span onClick={() => loadGame(game.id)}>
                    Game {game.id.slice(0, 8)}... 
                    <span className={`status-badge ${game.status}`}>{game.status}</span>
                  </span>
                  <button 
                    className="delete-btn"
                    onClick={() => deleteGame(game.id)}
                  >
                    ×
                  </button>
                </div>
              ))}
              {games.length === 0 && <p className="no-games">No games yet</p>}
            </div>
          </div>

          <div className="game-area">
            {currentGame ? (
              <>
                <div className="status">{getStatusMessage()}</div>
                <div className="board">
                  {Array.from({ length: 9 }, (_, i) => renderCell(i))}
                </div>
                <div className="game-info">
                  <p>Game ID: {currentGame.id}</p>
                  <p>Created: {new Date(currentGame.created_at).toLocaleString()}</p>
                </div>
              </>
            ) : (
              <div className="no-game">
                <p>Click "New Game" to start playing!</p>
              </div>
            )}
          </div>
        </div>

        {error && <div className="error-toast">{error}</div>}
      </div>
    </div>
  );
}

export default App;
