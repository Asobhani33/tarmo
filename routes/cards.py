# routes/cards.py
from flask import Blueprint, request, redirect, url_for
from bson import ObjectId
from db import get_db
from auth.decorators import login_required, board_access_required

cards_bp = Blueprint("cards", __name__)

@cards_bp.route("/list/<list_id>/cards/create", methods=["POST"])
@login_required
@board_access_required  # Decorator resolves board_id from list_id
def create_card(list_id):
    db = get_db()
    title = request.form["title"]
    
    lst = db.lists.find_one({"_id": ObjectId(list_id)})
    board_id = lst["board_id"]
    
    how_many_cards = db.cards.count_documents({"list_id": list_id})

    db.cards.insert_one({
        "name": name,
        "list_id": list_id,
        "board_id": board_id,
        "position": how_many_cards
    })

    return redirect(url_for("boards.view_board", board_id=board_id))
