-- Initialize the database
CREATE DATABASE IF NOT EXISTS demo;

-- Connect to the demo database
\c demo;

-- Create a table to demonstrate data persistence
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO messages (text, author) VALUES 
    ('Welcome to the Docker demo!', 'System'),
    ('This data persists in a Docker named volume.', 'System'),
    ('Try restarting the containers - your data will remain!', 'System');
