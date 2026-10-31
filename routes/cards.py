"""
routes/cards.py
-----------------
Owner: Person 2

Creating, moving, editing, and deleting cards. Also exposes a small helper
(`get_cards_for_list`) that Person 1's board.py template rendering uses.

TASKS FOR PERSON 2:
    1. create_card()      -> add a new card to a list
    2. move_card()         -> change a card's list_id (used by the drag & drop
                               JS that Person 4 writes — this is the endpoint
                               it calls)
    3. edit_card_title()    -> rename a card
    4. delete_card()          -> remove a card
    5. get_cards_for_list()    -> helper: returns all cards for a given list
                                   (not a route - a plain function other files call)
"""

from flask import Blueprint, request, jsonify, redirect, url_for
from bson import ObjectId
from db import get_db
from auth.decorators import login_required

cards_bp = Blueprint("cards", __name__)


@cards_bp.route("/card/create", methods=["POST"])
@login_required
def create_card():
    """
    TODO (Person 2): Create a new card.
    Steps:
        1. list_id = request.form.get("list_id")
        2. title = request.form.get("title")
        3. db = get_db()
        4. position = db["cards"].count_documents({"list_id": ObjectId(list_id)})
        5. db["cards"].insert_one({
               "list_id": ObjectId(list_id), "title": title, "description": "",
               "label": None, "due_date": None, "assigned_to": None,
               "comments": [], "archived": False, "position": position
           })
        6. Figure out the board_id (query the list) and redirect back to
           boards.view_board(board_id=board_id)
    """
    list_id = request.form.get("list_id")
    title = request.form.get("title")
    db = get_db()
    position = db["cards"].count_documents(
        {"list_id": ObjectId(list_id)}
    )
    db["cards"].insert_one({
        "list_id": ObjectId(list_id),
        "title": title,
        "description": "",
        "label": None,
        "due_date": None,
        "assigned_to": None,
        "completed": False,
        "checklist": [],
        "comments": [],
        "activity": [],
        "archived": False,
        "position": position
    })
    task_list = db["lists"].find_one({"_id": ObjectId(list_id)})
    return redirect(
        url_for("boards.view_board", board_id=str(task_list["board_id"]))
    )

@cards_bp.route("/card/<card_id>/move", methods=["POST"])
@login_required
def move_card(card_id):
    """
    TODO (Person 2): Move a card to a different list. This is a JSON AΡΙ endpoint (not a page redirect) because Person 4's drag-and-drop JS calls it with fetch() and expects a JSON response back.
    Steps:

        new_list_id = request.json.get("new_list_id")
        db = get_db()
        db["cards"].update_one( ) {"_id": ObjectId(card_id)}, {"$set": {"list_id": ObjectId(new_list_id)}}
        return jsonify({"success": True})
    """
    new_list_id = request.json.get("new_list_id")
    db = get_db()

    db["cards"].update_one(
        {"_id": ObjectId(card_id)},
        {"$set": {"list_id": ObjectId(new_list_id)}}
    )

    return jsonify({"success": True})


@cards_bp.route("/card/<card_id>/edit-title", methods=["POST"])
@login_required
def edit_card_title(card_id):
    """
    TODO (Person 2): Rename a card.
    Steps:
        1. new_title = request.form.get("title")
        2. db = get_db()
        3. db["cards"].update_one({"_id": ObjectId(card_id)}, {"$set": {"title": new_title}})
        4. Redirect back to the board it belongs to
    """
    new_title = request.form.get("title")
    db = get_db()
    card = db["cards"].find_one({"_id": ObjectId(card_id)})
    task_list = db["lists"].find_one({"_id": card["list_id"]})

    db["cards"].update_one(
        {"_id": ObjectId(card_id)},
        {"$set": {"title": new_title}}
    )

    return redirect(
        url_for("boards.view_board", board_id=str(task_list["board_id"]))
    )


@cards_bp.route("/card/<card_id>/delete", methods=["POST"])
@login_required
def delete_card(card_id):
    """
    TODO (Person 2): Delete a card.
    Steps:
        1. db = get_db()
        2. db["cards"].delete_one({"_id": ObjectId(card_id)})
        3. Redirect back to the board it belonged to
    """
    db = get_db()
    card = db["cards"].find_one({"_id": ObjectId(card_id)})
    task_list = db["lists"].find_one({"_id": card["list_id"]})
    db["cards"].delete_one({"_id": ObjectId(card_id)})

    return redirect(
        url_for("boards.view_board", board_id=str(task_list["board_id"]))
    )


def get_cards_for_list(list_id):
    """
    TODO (Person 2): Helper function (NOT a route) used by board.html rendering.
    Steps:
        1. db = get_db()
        2. return list(db["cards"].find(
               {"list_id": ObjectId(list_id), "archived": False}
           ).sort("position"))
    """
    db = get_db()
    return list(db["cards"].find(
        {"list_id": ObjectId(list_id), "archived": False}
    ).sort("position"))
