from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'xogame'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        port=os.environ.get('DB_PORT', '5432')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id VARCHAR(36) PRIMARY KEY,
            board VARCHAR(9) DEFAULT '         ',
            current_player CHAR(1) DEFAULT 'X',
            winner CHAR(1),
            status VARCHAR(20) DEFAULT 'ongoing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def check_winner(board):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != ' ':
            return board[pattern[0]]
    if ' ' not in board:
        return 'draw'
    return None

@app.route('/api/games', methods=['POST'])
def create_game():
    game_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO games (id, board, current_player, status) VALUES (%s, %s, %s, %s)',
        (game_id, '         ', 'X', 'ongoing')
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': game_id, 'board': '         ', 'current_player': 'X', 'status': 'ongoing'}), 201

@app.route('/api/games', methods=['GET'])
def get_games():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM games ORDER BY updated_at DESC')
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(game) for game in games])

@app.route('/api/games/<game_id>', methods=['GET'])
def get_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM games WHERE id = %s', (game_id,))
    game = cursor.fetchone()
    cursor.close()
    conn.close()
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(dict(game))

@app.route('/api/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    data = request.get_json()
    position = data.get('position')
    
    if position is None or not (0 <= position <= 8):
        return jsonify({'error': 'Invalid position'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM games WHERE id = %s', (game_id,))
    game = cursor.fetchone()
    
    if game is None:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Game not found'}), 404
    
    board = list(game['board'])
    
    if game['status'] != 'ongoing':
        cursor.close()
        conn.close()
        return jsonify({'error': 'Game is already finished'}), 400
    
    if board[position] != ' ':
        cursor.close()
        conn.close()
        return jsonify({'error': 'Position already taken'}), 400
    
    board[position] = game['current_player']
    new_board = ''.join(board)
    
    winner = check_winner(new_board)
    new_status = 'ongoing'
    next_player = 'O' if game['current_player'] == 'X' else 'X'
    
    if winner:
        new_status = 'finished'
        next_player = game['current_player']
    
    cursor.execute(
        '''UPDATE games SET board = %s, current_player = %s, winner = %s, status = %s, updated_at = CURRENT_TIMESTAMP 
           WHERE id = %s''',
        (new_board, next_player, winner if winner != 'draw' else None, new_status, game_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        'id': game_id,
        'board': new_board,
        'current_player': next_player,
        'winner': winner,
        'status': new_status
    })

@app.route('/api/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM games WHERE id = %s', (game_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Game deleted'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
