from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint("auth", __name__)


# -------------------------------------------------------
# REGISTER — create a new account
# -------------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Opening the page -> show the form
    if request.method == "GET":
        return render_template("register.html")

    db = get_db()
    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not username or not email or not password:
        flash("All fields are required.")
        return redirect(url_for("auth.register"))

    # Check for existing user by email or username
    if db.users.find_one({"$or": [{"email": email}, {"username": username}]}):
        flash("User with this email or username already exists.")
        return redirect(url_for("auth.register"))

    # The very first user of the site becomes the admin
    is_first_user = db.users.count_documents({}) == 0

    db.users.insert_one({
        "username": username,
        "email": email,
        "password_hash": generate_password_hash(password),   # never store plain text
        "role": "admin" if is_first_user else "member",
        "created_at": datetime.now(timezone.utc).isoformat(),
    })

    flash("Registration successful! Please log in.")
    return redirect(url_for("auth.login"))


# -------------------------------------------------------
# LOGIN — enter your account
# -------------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Step 1: If the user just opened the page -> show the form
    if request.method == "GET":
        return render_template("login.html")

    # Step 2: The user filled in the form and clicked Login
    db = get_db()
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    # Step 3: Look up that username in the database
    user = db.users.find_one({"username": username})

    # Step 4: Does the user exist AND does the password match?
    if user and check_password_hash(user.get("password_hash", ""), password):

        # Step 5: Save who is logged in (like a sticky note)
        session["user_id"]  = str(user["_id"])
        session["username"] = user["username"]
        session["role"]     = user.get("role", "member")

        # Step 6: Send them to their dashboard
        return redirect(url_for("boards.dashboard"))

    # Step 7: Wrong username or password
    flash("Wrong username or password. Try again.")
    return redirect(url_for("auth.login"))


# -------------------------------------------------------
# LOGOUT — leave your account
# -------------------------------------------------------
@auth_bp.route("/logout")
def logout():
    # Throw away the sticky note -> user is no longer logged in
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))