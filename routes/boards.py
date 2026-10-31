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
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from bson import ObjectId
from db import get_db
from auth.decorators import login_required, admin_required

boards_bp = Blueprint("boards", __name__)


@boards_bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()

    # Find every board where the user is the owner
    my_boards = list(db.boards.find({"owner_id": session["user_id"]}))

    # Show the dashboard page and pass the boards to it
    return render_template("dashboard.html", boards=my_boards)


# -------------------------------------------------------
# CREATE BOARD — make a new board
# -------------------------------------------------------
@boards_bp.route("/boards/create", methods=["POST"])
@login_required
def create_board():
    db = get_db()

    # Get the board name the user typed
    name = request.form["name"]

    # Save it to the database
    db.boards.insert_one({
        "name":    name,
        "owner_id": session["user_id"]
    })

    flash("Board created!")
    return redirect(url_for("boards.dashboard"))


# -------------------------------------------------------
# VIEW BOARD — open one board and see its lists + cards
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>")
@login_required
def view_board(board_id):
    db = get_db()

    # Load the board
    board = db.boards.find_one({"_id": ObjectId(board_id)})

    # Load all lists that belong to this board, in order
    lists = list(db.lists.find({"board_id": board_id}).sort("position", 1))

    # For each list, load its cards
    for one_list in lists:
        one_list["cards"] = list(db.cards.find({
            "list_id": str(one_list["_id"]),
            "archived": {"$ne": True}          # skip archived cards
        }).sort("position", 1))

    return render_template("board.html", board=board, lists=lists)


# -------------------------------------------------------
# DELETE BOARD — remove a board (only the owner can do this)
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>/delete", methods=["POST"])
@login_required
def delete_board(board_id):
    db = get_db()

    # Load the board and check the user is the owner
    board = db.boards.find_one({"_id": ObjectId(board_id)})
    if board["owner_id"] != session["user_id"]:
        flash("Only the owner can delete this board.")
        return redirect(url_for("boards.dashboard"))

    # Delete the board, its lists, and its cards
    db.boards.delete_one({"_id": ObjectId(board_id)})
    db.lists.delete_many({"board_id": board_id})
    db.cards.delete_many({"board_id": board_id})

    flash("Board deleted.")
    return redirect(url_for("boards.dashboard"))


# -------------------------------------------------------
# CREATE LIST — add a new column to a board
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>/lists/create", methods=["POST"])
@login_required
def create_list(board_id):
    db = get_db()

    name = request.form["name"]

    # Count existing lists so we know what position to give the new one
    how_many_lists = db.lists.count_documents({"board_id": board_id})

    db.lists.insert_one({
        "name":    name,
        "board_id": board_id,
        "position": how_many_lists    # goes at the end
    })

    return redirect(url_for("boards.view_board", board_id=board_id))


# -------------------------------------------------------
# DELETE LIST — remove a column and all its cards
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>/lists/<list_id>/delete", methods=["POST"])
@login_required
def delete_list(board_id, list_id):
    db = get_db()

    db.lists.delete_one({"_id": ObjectId(list_id)})
    db.cards.delete_many({"list_id": list_id})

    return redirect(url_for("boards.view_board", board_id=board_id))
