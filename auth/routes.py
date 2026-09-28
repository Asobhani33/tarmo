"""
auth/routes.py
----------------
Owner: Person 1

Registration, login, and logout. Passwords are NEVER stored in plain text —
always hashed with werkzeug's generate_password_hash / check_password_hash.

TASKS FOR PERSON 1:
    1. register()  -> create a new user document in the "users" collection
    2. login()     -> verify credentials, start a session
    3. logout()    -> clear the session

Test each of these using the pattern from the warm-up notebook (Part 5 & 6)
before wiring them to the real database.
"""

from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    TODO (Person 1): Register a new user.
    Steps:
        1. If GET request: just render the registration page
           (return render_template("register.html"))
        2. If POST request:
            a. Read "username" and "password" from request.form
            b. Check the username doesn't already exist in db["users"]
               (if it does, re-render the page with an error message)
            c. Hash the password: generate_password_hash(password)
            d. Insert a new document into db["users"]:
               {"username": username, "password_hash": ..., "role": "member"}
               (first registered user can be made "admin" manually in Mongo,
               or add a simple rule here for the very first user)
            e. Redirect to the login page: redirect(url_for("auth.login"))
    """
    if request.method == "GET":
        return render_template("register.html")

    # TODO: implement POST logic
    pass


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    TODO (Person 1): Log a user in.
    Steps:
        1. If GET request: render the login page
        2. If POST request:
            a. Read "username" and "password" from request.form
            b. Find the matching user in db["users"]
            c. If not found, or check_password_hash(user["password_hash"], password)
               is False -> re-render login page with an error
            d. If correct: store session["user_id"] = str(user["_id"])
               and session["role"] = user["role"]
            e. Redirect to the dashboard: redirect(url_for("boards.dashboard"))
    """
    if request.method == "GET":
        return render_template("login.html")

    # TODO: implement POST logic
    pass


@auth_bp.route("/logout")
def logout():
    """
    TODO (Person 1): Clear the session and redirect to login.
    Steps:
        1. session.clear()
        2. return redirect(url_for("auth.login"))
    """
    pass
