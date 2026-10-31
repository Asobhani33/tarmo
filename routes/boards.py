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
from auth.decorators import login_required, board_access_required, owner_required, get_role

boards_bp = Blueprint("boards", __name__)


# -------------------------------------------------------
# Part 1D: DASHBOARD — List own & shared boards with roles
# -------------------------------------------------------
@boards_bp.route("/")
@login_required
def dashboard():
    db = get_db()
    current_user_id = session["user_id"]

    # Query boards where user is in the members array or is legacy owner
    boards = list(db.boards.find({
        "$or": [
            {"members.user_id": current_user_id},
            {"owner_id": current_user_id}
        ]
    }))

    # Attach role to each board for UI label display
    for board in boards:
        board["user_role"] = get_role(board, current_user_id) or "member"

    return render_template("dashboard.html", boards=boards)


# -------------------------------------------------------
# Part 1A: CREATE BOARD — Save creator in members array as "owner"
# -------------------------------------------------------
@boards_bp.route("/boards/create", methods=["POST"])
@login_required
def create_board():
    db = get_db()
    name = request.form["name"]
    user_id = session["user_id"]

    db.boards.insert_one({
        "name": name,
        "members": [
            {"user_id": user_id, "role": "owner"}
        ]
    })

    flash("Board created!")
    return redirect(url_for("boards.dashboard"))


# -------------------------------------------------------
# VIEW BOARD — Protected by board_access_required
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>")
@login_required
@board_access_required
def view_board(board_id):
    db = get_db()

    board = db.boards.find_one({"_id": ObjectId(board_id)})
    lists = list(db.lists.find({"board_id": board_id}).sort("position", 1))

    for one_list in lists:
        one_list["cards"] = list(db.cards.find({
            "list_id": str(one_list["_id"]),
            "archived": {"$ne": True}
        }).sort("position", 1))

    return render_template("board.html", board=board, lists=lists)


# -------------------------------------------------------
# Part 1D: RENAME BOARD — POST /board/<board_id>/rename (Owner Only)
# -------------------------------------------------------
@boards_bp.route("/board/<board_id>/rename", methods=["POST"])
@login_required
@owner_required
def rename_board(board_id):
    db = get_db()
    new_title = request.form.get("title")

    db.boards.update_one(
        {"_id": ObjectId(board_id)},
        {"$set": {"title": new_title}}
    )

    return redirect(url_for("boards.view_board", board_id=board_id))


# -------------------------------------------------------
# DELETE BOARD — (Owner Only)
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>/delete", methods=["POST"])
@login_required
@owner_required
def delete_board(board_id):
    db = get_db()

    db.boards.delete_one({"_id": ObjectId(board_id)})
    db.lists.delete_many({"board_id": board_id})
    db.cards.delete_many({"board_id": board_id})

    flash("Board deleted.")
    return redirect(url_for("boards.dashboard"))


# -------------------------------------------------------
# CREATE LIST & Part 1D: RENAME LIST
# -------------------------------------------------------
@boards_bp.route("/boards/<board_id>/lists/create", methods=["POST"])
@login_required
@board_access_required
def create_list(board_id):
    db = get_db()
    name = request.form["name"]

    how_many_lists = db.lists.count_documents({"board_id": board_id})

    db.lists.insert_one({
        "name": name,
        "board_id": board_id,
        "position": how_many_lists
    })

    return redirect(url_for("boards.view_board", board_id=board_id))


@boards_bp.route("/list/<list_id>/rename", methods=["POST"])
@login_required
@board_access_required
def rename_list(list_id):
    db = get_db()
    new_title = request.form.get("title")

    list_item = db.lists.find_one({"_id": ObjectId(list_id)})
    if not list_item:
        flash("List not found.")
        return redirect(url_for("boards.dashboard"))

    db.lists.update_one(
        {"_id": ObjectId(list_id)},
        {"$set": {"title": new_title}}
    )

    return redirect(url_for("boards.view_board", board_id=list_item["board_id"]))


@boards_bp.route("/boards/<board_id>/lists/<list_id>/delete", methods=["POST"])
@login_required
@board_access_required
def delete_list(board_id, list_id):
    db = get_db()

    db.lists.delete_one({"_id": ObjectId(list_id)})
    db.cards.delete_many({"list_id": list_id})

    return redirect(url_for("boards.view_board", board_id=board_id))


# -------------------------------------------------------
# Part 1C: MEMBER MANAGEMENT ROUTES
# -------------------------------------------------------

# 1. POST /board/<board_id>/members (Form: email, role)
@boards_bp.route("/board/<board_id>/members", methods=["POST"])
@login_required
@board_access_required
def add_member(board_id):
    db = get_db()
    email = request.form.get("email")
    role = request.form.get("role", "member")

    board = db.boards.find_one({"_id": ObjectId(board_id)})

    # Look up user by email
    user_to_add = db.users.find_one({"email": email})
    if not user_to_add:
        flash("No user with this email")
        return redirect(url_for("boards.view_board", board_id=board_id))

    # Check if user is already a member
    already_member = any(
        str(m.get("user_id")) == str(user_to_add["_id"]) for m in board.get("members", [])
    )
    if already_member:
        flash("Already a member")
        return redirect(url_for("boards.view_board", board_id=board_id))

    # Add new member to members array
    db.boards.update_one(
        {"_id": ObjectId(board_id)},
        {"$push": {"members": {"user_id": str(user_to_add["_id"]), "role": role}}}
    )

    return redirect(url_for("boards.view_board", board_id=board_id))


# 2. POST /board/<board_id>/members/<user_id>/role
@boards_bp.route("/board/<board_id>/members/<user_id>/role", methods=["POST"])
@login_required
@board_access_required
def update_member_role(board_id, user_id):
    db = get_db()
    new_role = request.form.get("role")

    board = db.boards.find_one({"_id": ObjectId(board_id)})
    owners = [m for m in board.get("members", []) if m.get("role") == "owner"]

    # LAST OWNER DEMOTION GUARD
    is_target_owner = any(str(m.get("user_id")) == str(user_id) for m in owners)
    if is_target_owner and len(owners) <= 1 and new_role != "owner":
        flash("Cannot demote the last owner")
        return redirect(url_for("boards.view_board", board_id=board_id))

    # Update role
    db.boards.update_one(
        {"_id": ObjectId(board_id), "members.user_id": user_id},
        {"$set": {"members.$.role": new_role}}
    )

    return redirect(url_for("boards.view_board", board_id=board_id))


# 3. POST /board/<board_id>/members/<user_id>/remove
@boards_bp.route("/board/<board_id>/members/<user_id>/remove", methods=["POST"])
@login_required
@board_access_required
def remove_member(board_id, user_id):
    db = get_db()

    board = db.boards.find_one({"_id": ObjectId(board_id)})
    owners = [m for m in board.get("members", []) if m.get("role") == "owner"]

    # LAST OWNER REMOVAL GUARD
    is_target_owner = any(str(m.get("user_id")) == str(user_id) for m in owners)
    if is_target_owner and len(owners) <= 1:
        flash("Cannot remove the last owner")
        return redirect(url_for("boards.view_board", board_id=board_id))

    # Pull user out of members array
    db.boards.update_one(
        {"_id": ObjectId(board_id)},
        {"$pull": {"members": {"user_id": user_id}}}
    )

    return redirect(url_for("boards.view_board", board_id=board_id))