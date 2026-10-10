# MongoDB Schema (Person 4 owns, refine as needed)

MongoDB has no fixed schema, but we agree on a consistent document shape so
every route (written by different people) reads/writes data the same way.

Database name: `trello_clone` (set by `MONGO_DB_NAME` in `.env`)

## How the collections connect

```
users ──< boards ──< lists ──< cards
  │                              │
  └──────── assigned_to ─────────┘
```

- A **board** belongs to one user (`boards.owner_id` → `users._id`)
- A **list** belongs to one board (`lists.board_id` → `boards._id`)
- A **card** belongs to one list (`cards.list_id` → `lists._id`)
- A **card** can be assigned to one user (`cards.assigned_to` → `users._id`)

---

## Collection: `users`
```js
{
  "_id": ObjectId,
  "username": "ali",                        // unique
  "password_hash": "pbkdf2:sha256:...",     // NEVER store  passwords
  "role": "admin",                          // "admin" or "member"
  "created_at": "2026-09-28T12:00:00+00:00"
}
```

## Collection: `boards`
```js
{
  "_id": ObjectId,
  "name": "Website Redesign",
  "owner_id": ObjectId,                     // references users._id
  "created_at": "2026-09-28T12:00:00+00:00"
}
```

## Collection: `lists`
```js
{
  "_id": ObjectId,
  "board_id": ObjectId,                     // references boards._id
  "name": "To Do",
  "position": 0                             // order of the list on the board (0, 1, 2, ...)
}
```

## Collection: `cards`
```js
{
  "_id": ObjectId,
  "list_id": ObjectId,                      // references lists._id
  "title": "Design homepage",
  "description": "",                        // empty string when not set
  "label": { "name": "Design", "color": "#f97316" },   // or null
  "due_date": "2026-10-05",                 // "YYYY-MM-DD" or null
  "assigned_to": ObjectId,                  // references users._id, or null
  "comments": [                             // empty list [] when there are none
    { "author": "Yuliia", "text": "Looks good!", "created_at": "2026-09-28T13:00:00+00:00" }
  ],
  "archived": false,                        // archived cards are hidden from the board
  "position": 0                             // order of the card inside its list
}
```

A brand-new card (from `routes/cards.py` → `create_card()`) starts like this:

```js
{
  "list_id": ObjectId("..."),
  "title": "New card",
  "description": "",
  "label": null,
  "due_date": null,
  "assigned_to": null,
  "comments": [],
  "archived": false,
  "position": 3                             // = number of cards already in that list
}
```

`comments[].author` is the **username** (a string), not a user `_id`.

---

## Rules everyone follows

**1. IDs are `ObjectId` in the database, strings everywhere else.**
IDs that come from a URL (`/card/<card_id>/move`), a form, or JSON sent by
JavaScript are plain strings. Always convert them before querying, or the
query silently finds nothing:

```python
from bson import ObjectId

db["cards"].find_one({"_id": ObjectId(card_id)})      # correct
db["cards"].find_one({"_id": card_id})                # finds nothing
```

The same applies when saving references: store `ObjectId(list_id)`, not the string.

**2. Dates are ISO strings.**
- Timestamps (`created_at`):
  ```python
  from datetime import datetime, timezone
  datetime.now(timezone.utc).isoformat()
  ```
  (`datetime.utcnow()` still works but is deprecated in newer Python versions.)
- Calendar dates (`due_date`): `"YYYY-MM-DD"`, exactly as an HTML `<input type="date">` sends it.

**3. Empty values have one shape.**
Text fields default to `""`, list fields to `[]`, and optional references or
objects (`label`, `due_date`, `assigned_to`) to `null` / `None`. Don't leave
fields out of new documents; templates expect them to exist.

**4. Never delete what you can archive.**
Cards use `"archived": true` instead of being removed when a user archives them;
`delete_card()` is the only place that really deletes.

---

## Notes for Person 4
- `ObjectId` is Mongo's built-in unique ID type (`from bson import ObjectId`)
- Keep this file updated as Person 1 / Person 2 add fields their routes need
