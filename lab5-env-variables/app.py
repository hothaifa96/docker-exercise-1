from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

APP_NAME        = os.getenv("APP_NAME",        "Docker Config App")
ENVIRONMENT     = os.getenv("ENVIRONMENT",     "production")
SECRET_KEY      = os.getenv("SECRET_KEY",      "changeme-insecure")
DATABASE_URL    = os.getenv("DATABASE_URL",    "sqlite:///app.db")
MAX_ITEMS       = int(os.getenv("MAX_ITEMS",   "100"))
DARK_MODE       = os.getenv("FEATURE_DARK_MODE", "false").lower() == "true"
ADMIN_EMAIL     = os.getenv("ADMIN_EMAIL",     "admin@example.com")
APP_VERSION     = os.getenv("APP_VERSION",     "1.0")
CUSTOM_MESSAGE  = os.getenv("CUSTOM_MESSAGE",  "")

IS_DEV  = ENVIRONMENT == "development"
COLORS  = {"development": "#f0ad4e", "production": "#5cb85c", "staging": "#5bc0de"}
COLOR   = COLORS.get(ENVIRONMENT, "#777")


def mask_secret(val: str) -> str:
    """Show only first 3 chars + asterisks — never expose full secrets."""
    if not val or len(val) < 4:
        return "***"
    return val[:3] + "*" * (len(val) - 3)


@app.route("/")
def index():
    bg = "#1a1a2e" if DARK_MODE else "#f8f9fa"
    fg = "#e0e0e0" if DARK_MODE else "#212529"
    card = "#16213e" if DARK_MODE else "#ffffff"
    border = "#0f3460" if DARK_MODE else "#dee2e6"

    rows = [
        ("APP_NAME",            APP_NAME,                   "App title"),
        ("ENVIRONMENT",         ENVIRONMENT,                 f'<span style="color:{COLOR};font-weight:bold">{ENVIRONMENT}</span>'),
        ("APP_VERSION",         APP_VERSION,                 "Build version"),
        ("MAX_ITEMS",           str(MAX_ITEMS),              "Business logic limit"),
        ("FEATURE_DARK_MODE",   str(DARK_MODE).lower(),     "Feature flag"),
        ("ADMIN_EMAIL",         ADMIN_EMAIL,                 "Contact address"),
        ("SECRET_KEY",          mask_secret(SECRET_KEY),     "🔒 Masked for safety"),
        ("DATABASE_URL",        DATABASE_URL if IS_DEV else mask_secret(DATABASE_URL), "DB connection"),
        ("CUSTOM_MESSAGE",      CUSTOM_MESSAGE or "(not set)", "Your custom message"),
        ("HOSTNAME",            os.environ.get("HOSTNAME", "unknown"), "Container ID"),
    ]

    rows_html = "".join(
        f"<tr><td style='padding:8px 12px;font-family:monospace;color:#58a6ff'>{k}</td>"
        f"<td style='padding:8px 12px'>{v}</td>"
        f"<td style='padding:8px 12px;color:#888;font-size:0.85em'>{desc}</td></tr>"
        for k, v, desc in rows
    )

    debug_section = ""
    if IS_DEV:
        all_env = {k: v for k, v in sorted(os.environ.items())}
        env_list = "".join(f"<li><code>{k}={v}</code></li>" for k, v in all_env.items())
        debug_section = f"""
        <div style="margin-top:24px;background:{card};border:1px solid {border};border-radius:8px;padding:20px">
          <h2 style="color:#f0ad4e;margin-bottom:12px">🛠 Debug Mode (development only)</h2>
          <ul style="font-size:0.85em;list-style:none;column-count:2">{env_list}</ul>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head>
  <meta charset="UTF-8">
  <title>{APP_NAME}</title>
  <style>
    body{{background:{bg};color:{fg};font-family:'Segoe UI',Arial,sans-serif;margin:0;padding:24px}}
    h1{{color:#58a6ff}} table{{width:100%;border-collapse:collapse}}
    tr:hover{{background:rgba(88,166,255,0.05)}}
    th{{text-align:left;padding:8px 12px;color:#888;font-size:0.85em;border-bottom:1px solid {border}}}
  </style>
</head>
<body>
  <h1>⚙️ {APP_NAME}</h1>
  <p style="color:#888">Environment: <strong style="color:{COLOR}">{ENVIRONMENT}</strong>
     &nbsp;|&nbsp; Version: {APP_VERSION}
     &nbsp;|&nbsp; Dark Mode: {"✅" if DARK_MODE else "❌"}
     &nbsp;|&nbsp; {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC</p>
  {f'<div style="background:#1a472a;padding:10px 16px;border-radius:6px;margin:12px 0">💬 {CUSTOM_MESSAGE}</div>' if CUSTOM_MESSAGE else ""}
  <div style="background:{card};border:1px solid {border};border-radius:8px;padding:20px;margin-top:20px">
    <h2 style="margin-bottom:12px">Environment Variables</h2>
    <table>
      <thead><tr><th>Variable</th><th>Value</th><th>Description</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
  {debug_section}
  <p style="margin-top:24px;color:#555;font-size:0.85em">
    Admin: {ADMIN_EMAIL if IS_DEV else mask_secret(ADMIN_EMAIL)}
    &nbsp;|&nbsp; Lab 5 — Docker Environment Variables
  </p>
</body></html>"""


@app.route("/config")
def config_json():
    return jsonify({
        "app_name":    APP_NAME,
        "environment": ENVIRONMENT,
        "version":     APP_VERSION,
        "max_items":   MAX_ITEMS,
        "dark_mode":   DARK_MODE,
        "admin_email": ADMIN_EMAIL if IS_DEV else mask_secret(ADMIN_EMAIL),
        "secret_key":  mask_secret(SECRET_KEY),
        "database_url": DATABASE_URL if IS_DEV else mask_secret(DATABASE_URL),
        "container":   os.environ.get("HOSTNAME", "unknown"),
        "timestamp":   datetime.utcnow().isoformat()
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "environment": ENVIRONMENT})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Starting {APP_NAME} v{APP_VERSION}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Dark mode:   {DARK_MODE}")
    print(f"Port:        {port}")
    app.run(host="0.0.0.0", port=port, debug=IS_DEV)
