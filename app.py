"""
app.py
-------
Shared file (pre-built) — the Flask application entry point.

This is where the whole app comes together: it loads secrets from .env,
sets up the Flask app, and registers every person's routes as a "Blueprint"
(Flask's way of splitting routes across multiple files, which is exactly
why each person could work in their own file without touching this one).

Run the app with:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

# Load variables from .env into the environment (standard: secrets never
# hardcoded in source code, see .env.example for what's expected)
load_dotenv()

from auth.routes import auth_bp
from routes.boards import boards_bp
from routes.cards import cards_bp
from routes.card_details import card_details_bp
from routes.search_archive_reports import reports_bp


def create_app():
    app = Flask(__name__)

    # Secret key signs session cookies - must come from .env, never hardcoded
    app.secret_key = os.environ.get("SECRET_KEY")
    if not app.secret_key:
        raise RuntimeError(
            "SECRET_KEY is not set. Copy .env.example to .env and fill it in."
        )

    # Register each person's routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(boards_bp)
    app.register_blueprint(cards_bp)
    app.register_blueprint(card_details_bp)
    app.register_blueprint(reports_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
