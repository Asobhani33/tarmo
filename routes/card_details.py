# routes/card_details.py
from flask import Blueprint, render_template
from bson import ObjectId
from db import get_db
from auth.decorators import login_required, board_access_required

card_details_bp = Blueprint("card_details", __name__)

@card_details_bp.route("/card/<card_id>")
@login_required
@board_access_required  # Decorator resolves board_id from card_id
def view_card_details(card_id):
    db = get_db()
    card = db.cards.find_one({"_id": ObjectId(card_id)})
    return render_template("card_details.html", card=card)