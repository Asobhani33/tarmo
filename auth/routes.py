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
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint("auth", __name__)


# -------------------------------------------------------
# REGISTER — create a new account
# -------------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # Step 1: If the user just opened the page → show the form
    if request.method == "GET":
        return render_template("register.html")

    # Step 2: The user filled in the form and clicked Register
    db = get_db()
    username = request.form["username"]
    password = request.form["password"]

    # Step 3: Is that username already taken?
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        flash("That username is already taken. Try another one.")
        return redirect(url_for("auth.register"))

    # Step 4: Scramble the password so we never save the real one
    scrambled_password = generate_password_hash(password)

    # Step 5: Save the new user to the database
    db.users.insert_one({
        "username": username,
        "password": scrambled_password,
        "role": "member"
    })

    # Step 6: Done! Send them to the login page
    flash("Account created! Please log in.")
    return redirect(url_for("auth.login"))


# -------------------------------------------------------
# LOGIN — enter your account
# -------------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Step 1: If the user just opened the page → show the form
    if request.method == "GET":
        return render_template("login.html")

    # Step 2: The user filled in the form and clicked Login
    db = get_db()
    username = request.form["username"]
    password = request.form["password"]

    # Step 3: Look up that username in the database
    user = db.users.find_one({"username": username})

    # Step 4: Does the user exist AND does the password match?
    if user and check_password_hash(user["password"], password):

        # Step 5: Save who is logged in (like a sticky note)
        session["user_id"]  = str(user["_id"])
        session["username"] = user["username"]
        session["role"]     = user["role"]

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
    # Throw away the sticky note → user is no longer logged in
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
