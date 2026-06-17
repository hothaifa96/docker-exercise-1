import os
import time
import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
    )

def wait_for_db(retries=10, delay=3):
    for i in range(retries):
        try:
            conn = get_db()
            conn.close()
            print("Database connected.")
            return
        except Exception as e:
            print(f"Waiting for DB... ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database.")

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/notes", methods=["GET"])
def get_notes():
    search = request.args.get("search", "")
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if search:
        cursor.execute(
            "SELECT * FROM notes WHERE title LIKE %s ORDER BY updated_at DESC",
            (f"%{search}%",)
        )
    else:
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    for note in notes:
        if note.get("created_at"):
            note["created_at"] = note["created_at"].isoformat()
        if note.get("updated_at"):
            note["updated_at"] = note["updated_at"].isoformat()
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s)",
        (title, content)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id": new_id, "title": title, "content": content}), 201

@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notes SET title=%s, content=%s WHERE id=%s",
        (title, content, note_id)
    )
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"id": note_id, "title": title, "content": content})

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s", (note_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"message": "Note deleted"})

if __name__ == "__main__":
    wait_for_db()
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
