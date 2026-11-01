"""
db.py
------
Owner: Person 4 (Database)

MongoDB connection setup. This is PRE-BUILT (skeleton ready) so Person 1 and
Person 2 aren't blocked while Person 4 finishes the real Atlas cluster setup.

HOW IT WORKS:
    - The connection string (MONGO_URI) is read from the .env file, NEVER
      hardcoded here. This is a security standard: secrets never go in code
      that gets pushed to GitHub.
    - get_db() returns the database object. Every route file imports this
      and uses it to reach a collection, e.g. get_db()["cards"].

TASK FOR PERSON 4:
    1. Create a free MongoDB Atlas cluster (see README.md "Database Setup")
    2. Copy the real connection string into your own local .env file
       (never into this file, never into Git)
    3. Test the connection using test_connection() below
    4. Once confirmed working, help Person 1 & Person 2 wire their routes
       to real collections (they've been developing against this same
       interface, so nothing on their end should need to change)
    5. Design and document the schema for each collection in SCHEMA.md
       (users, boards, lists, cards) - a starting draft is in that file,
       refine it as the real fields get finalized by Person 1 & 2
"""

import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def get_db() -> Database:
    """
    Returns the MongoDB database object (creates the connection once,
    reuses it after that - this pattern is called a "singleton connection").
    """
    global _client, _db

    if _db is None:
        mongo_uri = os.environ.get("MONGO_URI")
        db_name = os.environ.get("MONGO_DB_NAME", "trello_clone")

        if not mongo_uri:
            raise RuntimeError(
                "MONGO_URI is not set. Copy .env.example to .env and fill in "
                "your real MongoDB Atlas connection string."
            )

        _client = MongoClient(mongo_uri)
        _db = _client[db_name]

    return _db


def test_connection():
    """
    Quick manual check that the connection actually works.
    Run with: python -c "from db import test_connection; test_connection()"
    """
    try:
        db = get_db()
        db.command("ping")
        print(f"Connected successfully to database: {db.name}")
    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    test_connection()


# ---------------------------------------------------------------------------
# V2 helper functions (Person 4, task A2)
# ---------------------------------------------------------------------------
from bson import ObjectId
from datetime import datetime, timezone


def _oid(value):
    """Return an ObjectId, whether we got a string or already an ObjectId."""
    return value if isinstance(value, ObjectId) else ObjectId(value)


def toggle_checklist_item(db, card_id, item_id):
    """
    Flip "done" of one checklist item.
    Returns the new value (True / False), or None if the card or item is missing.
    """
    card = db["cards"].find_one({"_id": _oid(card_id), "checklist.id": item_id})
    if card is None:
        return None
    item = next(i for i in card["checklist"] if i["id"] == item_id)
    new_value = not item["done"]
    db["cards"].update_one(
        {"_id": card["_id"], "checklist.id": item_id},
        {"$set": {"checklist.$.done": new_value}},
    )
    return new_value


def boards_for_user(db, user_id):
    """
    All boards where the user is a member (owner or member).
    members.user_id is stored as a string, like session["user_id"].
    """
    return list(db["boards"].find({"members.user_id": str(user_id)}))


def add_comment_db(db, card_id, user_id, author, text):
    """
    Add a comment to a card. Returns True when a card was changed.
    """
    result = db["cards"].update_one(
        {"_id": _oid(card_id)},
        {"$push": {"comments": {
            "user_id": str(user_id),
            "author": author,
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }}},
    )
    return result.modified_count == 1