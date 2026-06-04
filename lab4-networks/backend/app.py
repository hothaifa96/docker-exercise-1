from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

tasks = []
next_id = 1


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "tasks-backend",
        "container": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify({
        "count": len(tasks),
        "tasks": tasks,
        "server": os.environ.get("HOSTNAME", "unknown")
    })


@app.route("/api/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.json or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Missing 'title' field"}), 400

    task = {
        "id":         next_id,
        "title":      title,
        "priority":   data.get("priority", "medium"),
        "completed":  False,
        "created_at": datetime.utcnow().isoformat()
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.json or {}
    if "completed" in data:
        task["completed"] = bool(data["completed"])
    if "title" in data:
        task["title"] = data["title"].strip()
    task["updated_at"] = datetime.utcnow().isoformat()
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": f"Task {task_id} deleted"}), 200


@app.route("/api/stats")
def stats():
    done    = sum(1 for t in tasks if t["completed"])
    pending = len(tasks) - done
    return jsonify({
        "total":     len(tasks),
        "completed": done,
        "pending":   pending,
        "container": os.environ.get("HOSTNAME", "unknown")
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Tasks Backend starting on port {port}")
    app.run(host="0.0.0.0", port=port)
