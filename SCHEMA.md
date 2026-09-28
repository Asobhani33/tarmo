# MongoDB Schema (Draft — Person 4 owns, refine as needed)

MongoDB has no fixed schema, but we agree on a consistent document shape so
every route (written by different people) reads/writes data the same way.

## Collection: `users`
```json
{
  "_id": ObjectId,
  "username": "ali",
  "password_hash": "pbkdf2:sha256:...",   // NEVER store plain-text passwords
  "role": "admin",                          // "admin" or "member"
  "created_at": "2026-09-28T12:00:00Z"
}
```

## Collection: `boards`
```json
{
  "_id": ObjectId,
  "name": "Website Redesign",
  "owner_id": ObjectId,                      // references users._id
  "created_at": "2026-09-28T12:00:00Z"
}
```

## Collection: `lists`
```json
{
  "_id": ObjectId,
  "board_id": ObjectId,                      // references boards._id
  "name": "To Do",
  "position": 0                                // order of the list on the board
}
```

## Collection: `cards`
```json
{
  "_id": ObjectId,
  "list_id": ObjectId,                       // references lists._id
  "title": "Design homepage",
  "description": "",
  "label": { "name": "Design", "color": "#f97316" },
  "due_date": "2026-10-05",
  "assigned_to": ObjectId,                    // references users._id
  "comments": [
    { "author": "Yuliia", "text": "Looks good!", "created_at": "2026-09-28T13:00:00Z" }
  ],
  "archived": false,
  "position": 0
}
```

---

## Notes for Person 4
- `ObjectId` is Mongo's built-in unique ID type (`from bson import ObjectId`)
- Always store dates as ISO strings (`datetime.utcnow().isoformat()`) for consistency
- Keep this file updated as Person 1 / Person 2 add fields their routes need
