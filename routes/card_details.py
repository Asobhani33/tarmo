"""
routes/card_details.py
------------------------
Owner: Person 2

Everything that lives INSIDE a card once it's open: labels, due dates,
assignment, and comments.

TASKS FOR PERSON 2:
    1. add_label()        -> set a colored label on a card
    2. set_due_date()      -> set a due date
    3. assign_member()      -> assign the card to a user
    4. add_comment()          -> add a comment to a card
"""

from flask import Blueprint, request, redirect, url_for
from bson import ObjectId
from datetime import datetime
from db import get_db
from auth.decorators import login_required

card_details_bp = Blueprint("card_details", __name__)


@card_details_bp.route("/card/<card_id>/label", methods=["POST"])
@login_required
def add_label(card_id):
    """
    TODO (Person 2): Set a label on a card.
    Steps:
        1. name = request.form.get("label_name")
        2. color = request.form.get("label_color")
        3. db = get_db()
        4. db["cards"].update_one(
               {"_id": ObjectId(card_id)},
               {"$set": {"label": {"name": name, "color": color}}}
           )
        5. Redirect back to the board
    """
    pass


@card_details_bp.route("/card/<card_id>/due-date", methods=["POST"])
@login_required
def set_due_date(card_id):
    """
    TODO (Person 2): Set a due date on a card.
    Steps:
        1. due_date = request.form.get("due_date")   # e.g. "2026-10-05"
        2. db = get_db()
        3. db["cards"].update_one({"_id": ObjectId(card_id)}, {"$set": {"due_date": due_date}})
        4. Redirect back to the board
    """
    pass


@card_details_bp.route("/card/<card_id>/assign", methods=["POST"])
@login_required
def assign_member(card_id):
    """
    TODO (Person 2): Assign a card to a team member.
    Steps:
        1. user_id = request.form.get("user_id")
        2. db = get_db()
        3. db["cards"].update_one(
               {"_id": ObjectId(card_id)},
               {"$set": {"assigned_to": ObjectId(user_id)}}
           )
        4. Redirect back to the board
    """
    pass


@card_details_bp.route("/card/<card_id>/comment", methods=["POST"])
@login_required
def add_comment(card_id):
    """
    TODO (Person 2): Add a comment to a card.
    Steps:
        1. text = request.form.get("text")
        2. author = session.get("username")  (store username in session at login
           if not already, or look it up from user_id)
        3. db = get_db()
        4. db["cards"].update_one(
               {"_id": ObjectId(card_id)},
               {"$push": {"comments": {
                   "author": author, "text": text,
                   "created_at": datetime.utcnow().isoformat()
               }}}
           )
        5. Redirect back to the board
    """
    pass
