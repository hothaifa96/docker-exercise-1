"""
Lab 6 — Background Worker
Polls a Redis queue and processes incoming messages.
Demonstrates: env vars (Lab 5), volumes via log file (Lab 3),
               container DNS (Lab 4), and Compose scaling (Lab 6).
"""

import redis
import os
import json
import time
from datetime import datetime

REDIS_HOST       = os.getenv("REDIS_HOST",       "redis")
REDIS_PORT       = int(os.getenv("REDIS_PORT",   "6379"))
WORKER_ID        = os.getenv("WORKER_ID",        "worker-1")
PROCESS_INTERVAL = int(os.getenv("PROCESS_INTERVAL", "5"))
LOG_PATH         = os.getenv("LOG_PATH",         "/logs/worker.log")


def log(msg: str) -> None:
    line = f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] [{WORKER_ID}] {msg}"
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def connect_redis() -> redis.Redis:
    while True:
        try:
            r = redis.Redis(
                host=REDIS_HOST, port=REDIS_PORT,
                db=0, decode_responses=True, socket_timeout=3
            )
            r.ping()
            log(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return r
        except Exception as e:
            log(f"Redis not ready — retrying in 3s ({e})")
            time.sleep(3)


def process(msg_data: str) -> None:
    msg = json.loads(msg_data)
    log(f"Processing [{msg['id']}] from '{msg['author']}': {msg['text'][:60]}")
    time.sleep(0.3)
    log(f"Done [{msg['id']}]")


def main() -> None:
    log(f"Worker starting  (poll interval: {PROCESS_INTERVAL}s)")
    r = connect_redis()

    while True:
        try:
            item = r.lpop("pending_queue")
            if item:
                process(item)
            else:
                time.sleep(PROCESS_INTERVAL)
        except KeyboardInterrupt:
            log("Shutting down.")
            break
        except redis.ConnectionError as e:
            log(f"Redis connection lost: {e} — reconnecting...")
            r = connect_redis()
        except Exception as e:
            log(f"Unexpected error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
