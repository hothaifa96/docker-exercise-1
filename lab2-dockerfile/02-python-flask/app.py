import sys
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify(
        message='Hello from Python Flask running inside Docker!',
        app='flask-docker-lab',
        version='1.0.0'
    )


@app.route('/info')
def info():
    return jsonify(
        python_version=sys.version,
        language='Python',
        framework='Flask'
    )


@app.route('/health')
def health():
    return jsonify(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
