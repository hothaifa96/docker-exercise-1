-- XO Game Database Schema

CREATE TABLE IF NOT EXISTS games (
    id VARCHAR(36) PRIMARY KEY,
    board VARCHAR(9) DEFAULT '         ',
    current_player CHAR(1) DEFAULT 'X',
    winner CHAR(1),
    status VARCHAR(20) DEFAULT 'ongoing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_games_status ON games(status);
CREATE INDEX IF NOT EXISTS idx_games_updated_at ON games(updated_at DESC);
