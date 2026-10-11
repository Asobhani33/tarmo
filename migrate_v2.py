"""
migrate_v2.py
---------------
Owner: Person 4 (task A1)   |   Run ONCE, after SCHEMA.md V2 is merged.

Upgrades data created with Version 1 so that Version 2 code can read it:

    boards:  owner_id            ->  members: [{"user_id": owner_id, "role": "owner"}]
    cards:   missing fields      ->  checklist: [], activity: [], completed: False

USAGE:
    python migrate_v2.py

SAFE TO RUN TWICE: each step only touches documents that still need it.

TODO (Person 4):
    1. boards: find those that have "owner_id" and no "members".
       For each, update_one with $set members=[...] and $unset owner_id.
    2. cards: update_many({"checklist": {"$exists": False}},
                          {"$set": {"checklist": []}})
       and the same for "activity" (-> []) and "completed" (-> False).
    3. print how many documents were changed in each step.
"""

from db import get_db


def migrate():
    db = get_db()
    # TODO: write the three steps described above
    print("Nothing done yet - write the TODO steps first.")


if __name__ == "__main__":
    migrate()
