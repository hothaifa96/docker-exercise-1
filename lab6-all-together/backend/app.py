from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

APP_NAME   = os.getenv("APP_NAME",   "Docker Message Board")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
FLASK_ENV  = os.getenv("FLASK_ENV",  "production")


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0,
                       decode_responses=True, socket_timeout=3)


@app.route("/api/health")
def health():
    try:
        r = get_redis()
        r.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {e}"
    return jsonify({
        "status":    "healthy",
        "app":       APP_NAME,
        "redis":     redis_status,
        "container": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/api/messages", methods=["GET"])
def get_messages():
    try:
        r = get_redis()
        raw  = r.lrange("messages", 0, -1)
        msgs = [json.loads(m) for m in raw]
        msgs.reverse()
        return jsonify({
            "count":     len(msgs),
            "messages":  msgs,
            "container": os.environ.get("HOSTNAME", "unknown")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.route("/api/messages", methods=["POST"])
def post_message():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    msg = {
        "id":        str(uuid.uuid4())[:8],
        "text":      text,
        "author":    data.get("author", "Anonymous"),
        "timestamp": datetime.utcnow().isoformat(),
        "processed": False
    }

    try:
        r = get_redis()
        r.rpush("messages", json.dumps(msg))
        r.rpush("pending_queue", json.dumps(msg))
        return jsonify(msg), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.route("/api/messages/<msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    try:
        r = get_redis()
        all_msgs = r.lrange("messages", 0, -1)
        filtered = [m for m in all_msgs if json.loads(m).get("id") != msg_id]
        if len(filtered) == len(all_msgs):
            return jsonify({"error": "Message not found"}), 404
        r.delete("messages")
        for m in filtered:
            r.rpush("messages", m)
        return jsonify({"message": f"Deleted {msg_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 503


@app.route("/api/stats")
def stats():
    try:
        r = get_redis()
        total   = r.llen("messages")
        pending = r.llen("pending_queue")
        return jsonify({
            "total_messages": total,
            "pending_queue":  pending,
            "app":            APP_NAME,
            "environment":    FLASK_ENV,
            "redis_host":     REDIS_HOST
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 503


if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = FLASK_ENV == "development"
    print(f"Starting {APP_NAME}")
    print(f"Redis: {REDIS_HOST}:{REDIS_PORT}")
    app.run(host="0.0.0.0", port=port, debug=debug)
