"""
routes/search_archive_reports.py
-----------------------------------
Owner: Person 2

Searching cards, archiving instead of deleting, and simple board stats.

TASKS FOR PERSON 2:
    1. search_cards()      -> find cards by title keyword
    2. archive_card()       -> mark a card as archived (soft-delete)
    3. view_archived()       -> show all archived cards for a board
    4. board_stats()          -> simple counts: cards per list, total cards
"""

from flask import Blueprint, request, render_template, redirect, url_for
from bson import ObjectId
from db import get_db
from auth.decorators import login_required

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/board/<board_id>/search")
@login_required
def search_cards(board_id):
    """
    TODO (Person 2): Search cards by title within a board.
    Steps:
        1. keyword = request.args.get("q", "")
        2. db = get_db()
        3. Find all list_ids for this board, then find cards in those lists
           whose title contains the keyword (case-insensitive):
           db["cards"].find({
               "list_id": {"$in": list_ids},
               "title": {"$regex": keyword, "$options": "i"}
           })
        4. render_template("search_results.html", cards=results, board_id=board_id)
    """
    pass


@reports_bp.route("/card/<card_id>/archive", methods=["POST"])
@login_required
def archive_card(card_id):
    """
    TODO (Person 2): Archive a card instead of deleting it.
    Steps:
        1. db = get_db()
        2. db["cards"].update_one({"_id": ObjectId(card_id)}, {"$set": {"archived": True}})
        3. Redirect back to the board
    """
    pass


@reports_bp.route("/board/<board_id>/archived")
@login_required
def view_archived(board_id):
    """
    TODO (Person 2): Show all archived cards for a board.
    Steps:
        1. db = get_db()
        2. Find list_ids for the board, then cards with those list_ids AND archived=True
        3. render_template("archived.html", cards=results, board_id=board_id)
    """
    pass


@reports_bp.route("/board/<board_id>/stats")
@login_required
def board_stats(board_id):
    """
    TODO (Person 2): Show simple stats for a board.
    Steps:
        1. db = get_db()
        2. lists = list(db["lists"].find({"board_id": ObjectId(board_id)}))
        3. For each list, count cards: db["cards"].count_documents({"list_id": lst["_id"], "archived": False})
        4. total = sum of all counts
        5. render_template("stats.html", lists=lists, total=total)
    """
    pass
