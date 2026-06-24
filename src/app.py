"""
DevPulse — GitHub Activity Dashboard
Python/Flask version of the original Node.js/Express app.
"""

import os
import sys

# Allow imports from src/
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from dotenv import load_dotenv

from middleware.error_handler import register_error_handlers
from middleware.rate_limiter import limiter
from routes.github import github_bp

load_dotenv()

# ── App Setup ────────────────────────────────────────────────────────────────

app = Flask(__name__, static_folder=None)

# Security headers (equivalent to Helmet.js)
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response

# Rate limiter
limiter.init_app(app)

# Register blueprints
app.register_blueprint(github_bp, url_prefix="/api/github")

# Error handlers
register_error_handlers(app)

# ── Serve Frontend ───────────────────────────────────────────────────────────

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "..", "public")

@app.route("/")
def index():
    return send_from_directory(PUBLIC_DIR, "index.html")

# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    print(f"\n  DevPulse running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
