from flask import Flask, jsonify
import sys
import os
import platform
from datetime import datetime

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")


@app.route("/")
def index():
    return jsonify({
        "message": "Hello from Python Flask inside Docker!",
        "app_version": APP_VERSION,
        "environment": ENVIRONMENT,
        "container_id": os.environ.get("HOSTNAME", "unknown"),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/info")
def info():
    return jsonify({
        "python_version": sys.version,
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "hostname": os.environ.get("HOSTNAME", "unknown"),
        "working_dir": os.getcwd(),
        "environment_vars": {
            "APP_VERSION": APP_VERSION,
            "ENVIRONMENT": ENVIRONMENT,
            "PATH": os.environ.get("PATH", "")
        }
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "python-flask-app",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = ENVIRONMENT == "development"
    print(f"Starting Flask app v{APP_VERSION} on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
