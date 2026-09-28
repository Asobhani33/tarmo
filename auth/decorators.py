"""
auth/decorators.py
--------------------
Owner: Person 1

Middleware for protecting routes. This is PRE-BUILT and ready to use — import
these decorators in any route file that needs to require login or admin rights.

USAGE:
    from auth.decorators import login_required, admin_required

    @app.route("/create-card", methods=["POST"])
    @login_required
    def create_card():
        ...

    @app.route("/delete-board", methods=["POST"])
    @admin_required
    def delete_board():
        ...

HOW IT WORKS (standard Flask middleware pattern):
    A decorator wraps a route function and runs a check BEFORE the real
    view function executes. If the check fails, it returns an error response
    immediately and the real function never runs.

    We use Flask's `session` (a secure, signed cookie) to track who's logged
    in — this is set in auth/routes.py during login.
"""

from functools import wraps
from flask import session, jsonify, redirect, url_for


def login_required(f):
    """Blocks the route unless a user is logged in (session has 'user_id')."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """Blocks the route unless the logged-in user has role == 'admin'."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        if session.get("role") != "admin":
            return jsonify({"error": "Admins only"}), 403
        return f(*args, **kwargs)
    return wrapper
