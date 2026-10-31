"""
migrate_v2.py  (Person 4, task A1)
----------------------------------
Upgrades data created in V1 so that V2 code can read it. Run it ONCE.
It is safe to run twice: each step only touches documents that still need it.

    boards: adds members = [{user_id, role: "owner"}] built from owner_id
    cards:  adds checklist = [], activity = [], completed = False
    users:  only REPORTS who has no email (fill those by hand in Atlas)

owner_id is KEPT on purpose. Today's code still reads it (dashboard).
Remove it later, after P1-1 and P1-4 are merged.

USAGE:  python migrate_v2.py
"""

from db import get_db


def migrate():
    db = get_db()

    # --- what would change? (count only, nothing is written yet) ---
    boards_todo = db.boards.count_documents(
        {"owner_id": {"$exists": True}, "members": {"$exists": False}}
    )
    cards_no_checklist = db.cards.count_documents({"checklist": {"$exists": False}})
    cards_no_activity = db.cards.count_documents({"activity": {"$exists": False}})
    cards_no_completed = db.cards.count_documents({"completed": {"$exists": False}})
    users_no_email = list(db.users.find({"email": {"$exists": False}}, {"username": 1}))

    print("Boards that need members :", boards_todo)
    print("Cards without checklist  :", cards_no_checklist)
    print("Cards without activity   :", cards_no_activity)
    print("Cards without completed  :", cards_no_completed)
    print("Users without email      :", len(users_no_email))

    answer = input("Run the migration? (y/n) ").strip().lower()
    if answer != "y":
        print("Cancelled. Nothing was changed.")
        return

    # --- 1. boards: owner_id -> members ---
    changed = 0
    for board in db.boards.find(
        {"owner_id": {"$exists": True}, "members": {"$exists": False}}
    ):
        # user_id keeps the SAME type as owner_id (today a plain string)
        db.boards.update_one(
            {"_id": board["_id"]},
            {"$set": {"members": [{"user_id": board["owner_id"], "role": "owner"}]}},
        )
        changed += 1
    print("Boards updated:", changed)

    # --- 2. cards: new fields ---
    r1 = db.cards.update_many(
        {"checklist": {"$exists": False}}, {"$set": {"checklist": []}}
    )
    r2 = db.cards.update_many(
        {"activity": {"$exists": False}}, {"$set": {"activity": []}}
    )
    r3 = db.cards.update_many(
        {"completed": {"$exists": False}}, {"$set": {"completed": False}}
    )
    print("Cards updated: checklist", r1.modified_count,
          "| activity", r2.modified_count, "| completed", r3.modified_count)

    # --- 3. users without email: report only ---
    if users_no_email:
        print("Add an email by hand in Atlas for these users:")
        for u in users_no_email:
            print("  -", u.get("username", u["_id"]))

    print("Done.")


if __name__ == "__main__":
    migrate()