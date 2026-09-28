"""
routes/boards.py
------------------
Owner: Person 1

Boards, lists, and the multi-board dashboard.

TASKS FOR PERSON 1:
    1. dashboard()      -> show all boards belonging to the logged-in user
    2. create_board()   -> make a new board
    3. delete_board()   -> remove a board (admin only)
    4. view_board()     -> show one board with its lists and cards
    5. create_list()    -> add a new list (column) to a board
    6. delete_list()    -> remove a list

Every route here follows the same pattern:
    load data from Mongo -> (change it if needed) -> return/render a page
This is the same "load -> change -> save -> return" pattern from the
Library project, just using MongoDB instead of a JSON file.
"""

from flask import Blueprint, request, session, redirect, url_for, render_template
from bson import ObjectId
from db import get_db
from auth.decorators import login_required, admin_required

boards_bp = Blueprint("boards", __name__)


@boards_bp.route("/dashboard")
@login_required
def dashboard():
    """
    TODO (Person 1): Show all boards for the logged-in user.
    Steps:
        1. db = get_db()
        2. user_id = session["user_id"]
        3. boards = list(db["boards"].find({"owner_id": ObjectId(user_id)}))
        4. return render_template("dashboard.html", boards=boards)
    """
    pass


@boards_bp.route("/board/create", methods=["POST"])
@login_required
def create_board():
    """
    TODO (Person 1): Create a new board.
    Steps:
        1. name = request.form.get("name")
        2. db = get_db()
        3. db["boards"].insert_one({"name": name, "owner_id": ObjectId(session["user_id"])})
        4. return redirect(url_for("boards.dashboard"))
    """
    pass


@boards_bp.route("/board/<board_id>/delete", methods=["POST"])
@admin_required
def delete_board(board_id):
    """
    TODO (Person 1): Delete a board and its lists/cards.
    Steps:
        1. db = get_db()
        2. Find all list ids belonging to this board
        3. Delete all cards whose list_id is in those lists
        4. Delete all lists belonging to this board
        5. Delete the board itself: db["boards"].delete_one({"_id": ObjectId(board_id)})
        6. return redirect(url_for("boards.dashboard"))
    """
    pass


@boards_bp.route("/board/<board_id>")
@login_required
def view_board(board_id):
    """
    TODO (Person 1): Show one board with its lists (cards come from Person 2's
    cards.py — you can call a helper function they expose, e.g.
    from routes.cards import get_cards_for_list).
    Steps:
        1. db = get_db()
        2. board = db["boards"].find_one({"_id": ObjectId(board_id)})
        3. lists = list(db["lists"].find({"board_id": ObjectId(board_id)}).sort("position"))
        4. return render_template("board.html", board=board, lists=lists)
    """
    pass


@boards_bp.route("/board/<board_id>/list/create", methods=["POST"])
@login_required
def create_list(board_id):
    """
    TODO (Person 1): Add a new list (column) to a board.
    Steps:
        1. name = request.form.get("name")
        2. db = get_db()
        3. position = db["lists"].count_documents({"board_id": ObjectId(board_id)})
        4. db["lists"].insert_one({"board_id": ObjectId(board_id), "name": name, "position": position})
        5. return redirect(url_for("boards.view_board", board_id=board_id))
    """
    pass


@boards_bp.route("/list/<list_id>/delete", methods=["POST"])
@login_required
def delete_list(list_id):
    """
    TODO (Person 1): Delete a list and its cards.
    Steps:
        1. db = get_db()
        2. Find the list to get its board_id (for the redirect)
        3. db["cards"].delete_many({"list_id": ObjectId(list_id)})
        4. db["lists"].delete_one({"_id": ObjectId(list_id)})
        5. return redirect(url_for("boards.view_board", board_id=board_id))
    """
    pass
