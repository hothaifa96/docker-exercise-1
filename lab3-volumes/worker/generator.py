"""
Lab 3 — Worker Service
Generates random application logs and writes them to /logs/<date>.log
The /logs directory is shared with the backend via a Docker volume.
"""

import os
import time
import random
from datetime import datetime

LOG_DIR  = os.environ.get('LOG_DIR', '/logs')
INTERVAL = float(os.environ.get('INTERVAL', '2'))

LEVELS = ['INFO', 'INFO', 'INFO', 'WARN', 'ERROR']

SERVICES = ['auth-service', 'db-service', 'api-gateway', 'cache-service', 'scheduler']

MESSAGES = [
    ('INFO',  'User {user} logged in from {ip}'),
    ('INFO',  'Request GET /api/users completed in {ms}ms'),
    ('INFO',  'Cache hit for key: session:{id}'),
    ('INFO',  'Health check passed — all systems nominal'),
    ('INFO',  'Background job #{id} started'),
    ('INFO',  'Email sent to user {id}@example.com'),
    ('WARN',  'Cache miss for key: session:{id} — falling back to DB'),
    ('WARN',  'Response time {ms}ms exceeded threshold (500ms)'),
    ('WARN',  'Retry attempt {id} of 3 for job #{id}'),
    ('WARN',  'Disk usage at {pct}% on /data partition'),
    ('ERROR', 'Database connection timeout after {ms}ms'),
    ('ERROR', 'Unhandled exception in {service} — NullPointerException'),
    ('ERROR', 'Failed to reach upstream {service} after 3 retries'),
]


def rand_values():
    return {
        'user':    f'user_{random.randint(100, 999)}',
        'ip':      f'192.168.{random.randint(0, 255)}.{random.randint(1, 254)}',
        'ms':      random.randint(12, 1800),
        'id':      random.randint(1000, 9999),
        'pct':     random.randint(70, 95),
        'service': random.choice(SERVICES),
    }


def format_message(template, values):
    try:
        return template.format(**values)
    except KeyError:
        return template


os.makedirs(LOG_DIR, exist_ok=True)
print(f'[worker] Log generator started — writing to {LOG_DIR} every {INTERVAL}s', flush=True)

while True:
    level_hint, template = random.choice(MESSAGES)
    level   = random.choice(['INFO', 'INFO', level_hint])
    service = random.choice(SERVICES)
    values  = rand_values()
    message = format_message(template, values)

    now       = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    date_str  = now.strftime('%Y-%m-%d')
    log_line  = f'[{timestamp}] [{level:<5}] [{service}] {message}\n'

    log_file = os.path.join(LOG_DIR, f'app-{date_str}.log')
    with open(log_file, 'a') as f:
        f.write(log_line)

    print(log_line.strip(), flush=True)
    time.sleep(INTERVAL)
