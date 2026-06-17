from flask import Flask, send_from_directory, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)
PORT = 8080
DATA_DIR = '/data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Serve static files from data directory
@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(DATA_DIR, filename)

# List all available files
@app.route('/api/files')
def list_files():
    try:
        files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith('.json')], reverse=True)
        return jsonify({'files': files, 'count': len(files)})
    except Exception as e:
        return jsonify({'error': 'Failed to list files'}), 500

# Get file metadata
@app.route('/api/files/<filename>')
def get_file_metadata(filename):
    try:
        filepath = os.path.join(DATA_DIR, filename)
        stats = os.stat(filepath)
        
        with open(filepath, 'r') as f:
            content = json.load(f)
        
        return jsonify({
            'filename': filename,
            'size': stats.st_size,
            'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'data': content
        })
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'dataDir': DATA_DIR})

if __name__ == '__main__':
    print(f'File server running on port {PORT}')
    print(f'Serving files from: {DATA_DIR}')
    print(f'Access files at: http://localhost:{PORT}/files/<filename>')
    print(f'List files at: http://localhost:{PORT}/api/files')
    app.run(host='0.0.0.0', port=PORT)
