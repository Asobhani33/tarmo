from functools import wraps
from flask import session, redirect, url_for, abort, request
from bson import ObjectId
from db import get_db

# -------------------------------------------------------
# Part 1A: get_role helper
# -------------------------------------------------------
def get_role(board, user_id):
    """
    Returns 'owner', 'member', or None based on the user's role in the board.
    Handles ObjectId vs string comparisons and legacy owner_id schema.
    """
    if not board or not user_id:
        return None
        
    members = board.get("members", [])
    for m in members:
        if str(m.get("user_id")) == str(user_id):
            return m.get("role", "member")
            
    # Fallback check for legacy owner_id
    if str(board.get("owner_id")) == str(user_id):
        return "owner"
        
    return None


# -------------------------------------------------------
# Part 1B: Decorators
# -------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def _get_board_from_request_args(db, kwargs):
    """Helper to locate the parent board_id from board_id, list_id, or card_id parameters."""
    board_id = kwargs.get("board_id")
    if board_id:
        return board_id

    list_id = kwargs.get("list_id")
    card_id = kwargs.get("card_id")

    if list_id:
        try:
            lst = db.lists.find_one({"_id": ObjectId(list_id)})
            if lst:
                return lst.get("board_id")
        except Exception:
            return None

    if card_id:
        try:
            card = db.cards.find_one({"_id": ObjectId(card_id)})
            if card:
                lst = db.lists.find_one({"_id": ObjectId(card.get("list_id"))})
                if lst:
                    return lst.get("board_id")
        except Exception:
            return None

    return None


def board_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = get_db()
        board_id = _get_board_from_request_args(db, kwargs)

        if not board_id:
            abort(404)

        try:
            board = db.boards.find_one({"_id": ObjectId(board_id)})
        except Exception:
            abort(404)

        if not board:
            abort(404)

        current_user_id = session.get("user_id")
        role = get_role(board, current_user_id)

        # Non-members get 403 Forbidden
        if role is None:
            abort(403)

        return f(*args, **kwargs)
    return decorated_function


def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = get_db()
        board_id = _get_board_from_request_args(db, kwargs)

        if not board_id:
            abort(404)

        try:
            board = db.boards.find_one({"_id": ObjectId(board_id)})
        except Exception:
            abort(404)

        if not board:
            abort(404)

        current_user_id = session.get("user_id")
        role = get_role(board, current_user_id)

        # Only owners pass
        if role != "owner":
            abort(403)

        return f(*args, **kwargs)
    return decorated_function