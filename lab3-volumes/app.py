from flask import Flask, jsonify, request, send_file
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)

DATA_DIR  = os.getenv("DATA_DIR", "/data")
DATA_FILE = os.path.join(DATA_DIR, "notes.json")


def load_notes():
    """Load notes from the data file (on the volume)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    """Save notes to the data file (on the volume)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)


@app.route("/")
def index():
    notes = load_notes()
    hostname = os.environ.get("HOSTNAME", "unknown")
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Notes App</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }}
    h1 {{ color: #0066cc; }}
    .note {{ background: #f4f4f4; border-left: 4px solid #0066cc; padding: 12px; margin: 10px 0; border-radius: 4px; }}
    .meta {{ color: #666; font-size: 0.85em; }}
    form {{ margin-bottom: 20px; }}
    input, textarea {{ width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }}
    button {{ background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 4px; }}
    .info {{ background: #e8f4fd; padding: 10px; border-radius: 4px; margin-bottom: 20px; font-size: 0.9em; }}
  </style>
</head>
<body>
  <h1>📝 Docker Notes App</h1>
  <div class="info">
    <strong>Container:</strong> {hostname} &nbsp;|&nbsp;
    <strong>Data file:</strong> {DATA_FILE} &nbsp;|&nbsp;
    <strong>Notes:</strong> {len(notes)}
  </div>
  <form method="POST" action="/notes-form">
    <input name="author" placeholder="Your name" required>
    <textarea name="text" rows="3" placeholder="Write a note..." required></textarea>
    <button type="submit">Add Note</button>
  </form>
  <h2>Notes ({len(notes)} total)</h2>
  {"".join(f'<div class="note"><p>{n["text"]}</p><p class="meta">By <b>{n["author"]}</b> at {n["created_at"][:19]} | ID: {n["id"]}</p></div>' for n in reversed(notes)) or "<p>No notes yet.</p>"}
</body>
</html>"""
    return html


@app.route("/notes-form", methods=["POST"])
def add_note_form():
    """Handle HTML form submission."""
    notes = load_notes()
    note = {
        "id":         str(uuid.uuid4())[:8],
        "text":       request.form.get("text", "").strip(),
        "author":     request.form.get("author", "Anonymous").strip(),
        "created_at": datetime.utcnow().isoformat()
    }
    notes.append(note)
    save_notes(notes)
    from flask import redirect
    return redirect("/")


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = load_notes()
    return jsonify({
        "count":     len(notes),
        "data_file": DATA_FILE,
        "container": os.environ.get("HOSTNAME", "unknown"),
        "notes":     notes
    })


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    notes = load_notes()
    note = {
        "id":         str(uuid.uuid4())[:8],
        "text":       text,
        "author":     data.get("author", "Anonymous"),
        "created_at": datetime.utcnow().isoformat()
    }
    notes.append(note)
    save_notes(notes)
    return jsonify(note), 201


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes = load_notes()
    updated = [n for n in notes if n["id"] != note_id]
    if len(updated) == len(notes):
        return jsonify({"error": "Note not found"}), 404
    save_notes(updated)
    return jsonify({"message": f"Note {note_id} deleted"}), 200


@app.route("/export")
def export_notes():
    """Download notes as a plain text file."""
    notes = load_notes()
    lines = [f"Docker Notes Export — {datetime.utcnow().isoformat()}\n", "=" * 50 + "\n"]
    for n in notes:
        lines.append(f"\n[{n['created_at'][:19]}] {n['author']}:\n{n['text']}\n")
    content = "".join(lines)
    from io import BytesIO
    buf = BytesIO(content.encode())
    buf.seek(0)
    return send_file(buf, mimetype="text/plain",
                     as_attachment=True, download_name="notes.txt")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Notes App starting on port {port}")
    print(f"Data directory: {DATA_DIR}")
    app.run(host="0.0.0.0", port=port)
