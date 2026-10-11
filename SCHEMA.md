# MongoDB Schema (Person 4 owns, refine as needed)

**Current version: V2** (plan: `docs/v2/TASKS.md`). Lines marked `// V2` are new in version 2.

MongoDB has no fixed schema, but we agree on a consistent document shape so
every route (written by different people) reads/writes data the same way.

Database name: `trello_clone` (set by `MONGO_DB_NAME` in `.env`)

## How the collections connect

```
users >──< boards ──< lists ──< cards
  │                              │
  └──────── assigned_to ─────────┘
```

- A **board** has several members, each with a role (`boards.members[].user_id` → `users._id`). V2: this replaces `owner_id`.
  A user can be in many boards, a board has many users, so it is many-to-many.
- A **list** belongs to one board (`lists.board_id` → `boards._id`)
- A **card** belongs to one list (`cards.list_id` → `lists._id`)
- A **card** can be assigned to one user (`cards.assigned_to` → `users._id`)

---

## Collection: `users`
```js
{
  "_id": ObjectId,
  "username": "ali",                        // unique
  "email": "ali@example.com",               // V2: unique, used to invite people to a board
  "password_hash": "pbkdf2:sha256:...",     // NEVER store  passwords
  "role": "admin",                          // site role: "admin" or "member". V2: the first registered user is the admin
  "created_at": "2026-09-28T12:00:00+00:00"
}
```

## Collection: `boards`
```js
{
  "_id": ObjectId,
  "name": "Website Redesign",
  "members": [                              // V2: replaces "owner_id"
    { "user_id": ObjectId, "role": "owner" },     // references users._id; role: "owner" or "member"
    { "user_id": ObjectId, "role": "member" }
  ],                                        // a board always has at least ONE owner
  "created_at": "2026-09-28T12:00:00+00:00"
}
```

Board roles: an **owner** can invite, change roles, remove members, rename and delete the board.
A **member** can work with lists and cards but cannot manage people.
(The site role in `users.role` is separate: it only says who is the site admin.)

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
  "completed": false,                       // V2: the tick on the card
  "checklist": [                            // V2: empty list [] when there are none
    { "id": 1, "text": "Sketch wireframe", "done": true },
    { "id": 2, "text": "Pick fonts", "done": false }     // id = highest id in this list + 1 (1 for the first item)
  ],
  "comments": [                             // empty list [] when there are none
    { "user_id": ObjectId, "author": "Yuliia", "text": "Looks good!", "created_at": "2026-09-28T13:00:00+00:00" }
    // V2: "user_id" is new. "author" stays (the username)
  ],
  "activity": [                             // V2: lines written by the system, [] when none
    { "user_id": ObjectId, "action": "moved this card to Done", "created_at": "2026-09-28T14:00:00+00:00" }
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
  "completed": false,                       // V2
  "checklist": [],                          // V2
  "comments": [],
  "activity": [],                           // V2
  "archived": false,
  "position": 3                             // = number of cards already in that list
}
```

`comments[].author` is the **username** (a string); `comments[].user_id` (V2) is the user `_id`.
The progress of a checklist is never stored: it is calculated (`done` items / all items).

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

**5. (V2) Every board route checks the board access first.**
Look up `board["members"]` and compare the user id as strings. Not logged in: redirect to login.
Logged in but not a member: **403**. Board does not exist: **404**. Cards and lists belong to a
board, so find the board from the card's list first.

**6. (V2) The last owner of a board can never be removed or demoted.**

**7. (V2) New cards and boards start complete.**
Use the "brand-new card" shape above and `members: [{creator, "owner"}]` for a new board,
so templates never meet a missing field.

---

## V2 migration (run once)

Data created in V1 is upgraded with `python migrate_v2.py` (Person 4, task A1):

| Collection | Before (V1) | After (V2) |
|---|---|---|
| `boards` | `owner_id` | `members: [{user_id: <owner_id>, role: "owner"}]`, `owner_id` removed |
| `cards` | no `completed`, `checklist`, `activity` | `completed: false`, `checklist: []`, `activity: []` |
| `users` | no `email` | add the email by hand for old users (needed to invite them) |

The script must be safe to run twice (only change documents that still need it).

---

## Notes for Person 4
- `ObjectId` is Mongo's built-in unique ID type (`from bson import ObjectId`)
- Keep this file updated as Person 1 / Person 2 add fields their routes need
