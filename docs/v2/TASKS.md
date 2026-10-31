# Tarmo V2: Task Plan

Planned by the Project Manager (Ali). Version 2 adds **sharing a board with teammates**, **checklists**, **comments**, and **filters**, and fixes some gaps from V1.

> Do your role's warm-up first: `Tarmo_V2_Warmup.ipynb` (Person 1, 2, 4) or `Person3_V2_Frontend_Warmup.html` (Person 3).
> Any change to the file structure or to this plan must be confirmed with the Project Manager.

---

## 0. Shared agreements (everyone reads this)

### 0.1 New data shapes (MongoDB)

```python
# Fields in CAPITALS-free style = new in V2. Everything else is unchanged from V1 (see SCHEMA.md).
boards: { "_id", "name",
          "members": [ {"user_id": ObjectId, "role": "owner" | "member"} ] }      # NEW (replaces owner_id)
users:  { ..., "email": "ali@example.com" }                                         # NEW (needed to invite)
cards:  { "_id", "list_id", "title", "description", "label", "due_date",
          "assigned_to", "archived", "position",                                    # same as V1
          "completed": False,                                                       # NEW
          "checklist": [ {"id": 1, "text": "...", "done": False} ],                 # NEW
          "comments":  [ {"user_id", "author", "text", "created_at"} ],             # user_id is NEW
          "activity":  [ {"user_id", "action", "created_at"} ] }                    # NEW
```
The warm-up notebook uses shorter names (`due`, `labels`) so the exercises stay small. In the real project use the names above and in `SCHEMA.md`.

`boards.owner_id` from V1 is replaced by `members` (Person 4 migrates old boards, see task A1: `migrate_v2.py`).

### 0.2 API contract (the promise between backend and frontend/JS)

| Route | Method | Sends | Returns (JSON) | Built by | Used by |
|---|---|---|---|---|---|
| `/card/<id>/json` | GET | nothing | the whole card incl. checklist, comments, activity | Person 2 | Person 4 (dialog) |
| `/card/<id>/complete` | POST | nothing | `{"completed": true}` | Person 2 | Person 4 |
| `/card/<id>/description` | POST | `{"description": "..."}` | `{"description": "..."}`; 400 if missing | Person 2 | Person 4 |
| `/card/<id>/checklist` | POST | `{"text": "..."}` | `{"id": 3, "done": 2, "total": 4, "percent": 50}` | Person 2 | Person 4 |
| `/card/<id>/checklist/<item_id>/toggle` | POST | nothing | `{"done": 3, "total": 4, "percent": 75}` | Person 2 | Person 4 |
| `/card/<id>/checklist/<item_id>/delete` | POST | nothing | same as toggle | Person 2 | Person 4 |
| `/card/<id>/comment` | POST | `{"text": "..."}` | the new comment; 400 if empty | Person 2 | Person 4 |
| `/board/<id>/members` | POST (form) | `email`, `role` | redirect with flash message | Person 1 | Person 3 (form) |
| `/board/<id>/members/<uid>/role` | POST (form) | `role` | redirect | Person 1 | Person 3 |
| `/board/<id>/members/<uid>/remove` | POST (form) | nothing | redirect | Person 1 | Person 3 |

If a route's shape has to change, tell everyone in the group first.

### 0.3 Branch and PR rules
- Branch name: `yourname-taskname`, for example `mamur-checklist-ui`.
- One task = one branch = one Pull Request.
- Never commit `.env`. Pull `main` before you start every new task.
- Write `Closes #<issue number>` in the PR description.

### 0.4 Order of work

| Week | Goal | Who |
|---|---|---|
| 1 | Fix V1 gaps, new data shapes, board membership | Person 1, Person 2, Person 4 (Person 3 starts HTML with fake data) |
| 2 | Checklist, comments, filter (backend + JS + HTML together) | everyone |
| 3 | Share dialog, phone layout, full test, cleanup | everyone |

---

## Person 1 (Silent): Backend, people and boards

Files: `auth/decorators.py`, `auth/routes.py`, `routes/boards.py`. Warm-up: Part 1.

### P1-1. Board membership and `get_role`
- **Why:** in V1 anyone could open any board. Every V2 feature needs to know who is in a board and with which role.
- **Where:** `auth/decorators.py` (helper `get_role(board, user_id)`), `routes/boards.py` (when a board is created, add the creator as `{"user_id": ..., "role": "owner"}` in `members`).
- **Steps:** write `get_role`; change `create_board` to fill `members`; stop using `owner_id`.
- **Depends on:** P4 task A1 (schema agreed).
- **Done when:** a new board has the creator as owner, and `get_role` returns `owner`, `member` or `None`.

### P1-2. `board_member_required` and `owner_required` decorators
- **Why:** one line above a route instead of copying an `if` into 15 routes.
- **Where:** `auth/decorators.py`. Apply them in `routes/boards.py`, `cards.py`, `card_details.py`.
- **Steps:** member not logged in: redirect to login. Logged in but not a member: **403**. Unknown board: **404**. `owner_required` allows only the owner.
- **Done when:** user B cannot open user A's board by typing the URL (403), and the owner can.
- **Remember:** cards and lists also belong to a board, so look up the board from the card or list first.

### P1-3. Invite, change role, remove member (owner only)
- **Why:** this is the Share dialog. The owner types an email and picks a role.
- **Where:** `routes/boards.py`. Routes in the table above (section 0.2).
- **Rules:** unknown email gives the message "No user with this email"; same person twice gives "Already a member"; **the last owner can never be removed or demoted**; use `flash()` for messages.
- **Depends on:** P1-2.
- **Done when:** all four rules work in the browser and Mamur's form posts to your routes.

### P1-4. Dashboard shows only my boards, rename board
- **Why:** after sharing, a user should see boards they own and boards they were invited to.
- **Where:** `routes/boards.py`, query `db.boards.find({"members.user_id": user_id})`.
- **Also:** `POST /board/<id>/rename` (owner only) and `POST /list/<id>/rename`.
- **Done when:** the dashboard lists both own and shared boards, with the role shown as a small label.

---

## Person 2 (Yuliia): Backend, cards

Files: `routes/cards.py`, `routes/card_details.py`, `routes/search_archive_reports.py`. Warm-up: Part 2.

### P2-1. Missing V1 routes
- **Why:** the card dialog is filled by JavaScript, which needs data as JSON. These routes were left out of the V1 starter.
- **Where:** `routes/card_details.py`.
- **Steps:** `GET /card/<id>/json`; `POST /card/<id>/description`; `POST /card/<id>/complete` (toggle `completed`); `POST /card/<id>/copy` (new card in the same list, title + " (copy)").
- **Done when:** each route works with `board_member_required` (a non-member gets 403) and the JSON shape matches section 0.2.

### P2-2. Checklist API
- **Why:** Mamur shows the checklist and the badge "2/5"; Ali's JS ticks items. You make the data and the percent.
- **Where:** `routes/card_details.py`. Routes in section 0.2.
- **Steps:** add item (id = highest id + 1), toggle, delete; every route returns `{"done", "total", "percent"}`; an empty checklist gives `0, 0, 0` (no division by zero).
- **Depends on:** P2-1, P4 task A2 (DB helpers).
- **Done when:** ticking an item changes `percent`; the numbers are right in the JSON.

### P2-3. Comments and activity log
- **Why:** the "Comments and activity" panel. Comments are written by people; activity lines are written by the system.
- **Where:** `routes/card_details.py`.
- **Steps:** `POST /card/<id>/comment` (400 if text is empty, trim spaces); a helper `log_activity(card_id, user_id, action)` called when a card is moved, ticked, assigned or completed; `GET /card/<id>/json` returns a merged timeline, newest first, with a `kind` field.
- **Done when:** moving a card adds an activity line, a comment appears first.

### P2-4. Filter and search
- **Why:** the filter bar.
- **Where:** `routes/search_archive_reports.py`.
- **Steps:** `GET /board/<id>/cards?text=&member=&label=&due_before=` (Mongo fields: `title`, `assigned_to`, `label.name`, `due_date`); empty filters are ignored; return JSON or render with the same template.
- **Done when:** every combination of the four filters gives the right cards.

---

## Person 3 (Mamur): HTML, CSS, Tailwind, Jinja

Files: `templates/*.html`, `static/css/style.css`. Warm-up: `Person3_V2_Frontend_Warmup.html`. Design: the wireframe (orange numbers 1 to 6).

Start with **fake data in the template** (hard-coded Jinja variables), so you are not blocked by the backend.

### P3-1 (wireframe 1). Checklist section in the card dialog
- **Why:** shows what is left to do inside a card.
- **Where:** `templates/board.html` (card dialog). IDs for JS: `#checklist`, `#bar`, `#checklist-form`.
- **Build:** title "Checklist", progress bar (width = percent), one checkbox per item, an "Add an item" input with Add button.
- **Done when:** with 2 of 5 items done the bar is 40 percent wide and items that are done look crossed out.

### P3-2 (wireframe 2). Checklist badge on the card
- **Where:** the card markup in `templates/board.html`.
- **Build:** small grey badge with an icon and `2/5`; hide the badge if the checklist is empty. Same for the comment count and the due date badge.
- **Done when:** badges line up and wrap nicely on a narrow card.

### P3-3 (wireframe 3). Comments and activity panel
- **Where:** right side of the card dialog.
- **Build:** a textarea and Save button; comments as bubbles with avatar initials; activity as small grey text lines; newest first.
- **Done when:** with 0 comments an empty message is shown, with 20 the panel scrolls.

### P3-4 (wireframe 4). Share button and Share dialog
- **Where:** navbar in `base.html`/`board.html` plus the dialog.
- **Build:** Share button (owners only: `{% if role == "owner" %}`); dialog with invite form (email, role select, Invite button) and a member list with role select and Remove button. Members see the list **without** the form and buttons.
- **Depends on:** P1-3 (form field names `email`, `role`).
- **Done when:** the owner view and the member view both match the wireframe.

### P3-5 (wireframe 5). Filter bar
- **Where:** under the navbar in `templates/board.html`.
- **Build:** search input, three dropdowns (Member, Label, Due date), "Clear filters" link. Give inputs ids (`#search`, `#filter-member`, ...) for Ali's JS.
- **Done when:** the bar wraps to two lines on a small screen without breaking.

### P3-6 (wireframe 6). Phone layout and dark mode (dark mode is optional)
- **Build:** one column visible and swipe sideways on a phone; buttons at least 44 px; Tailwind `dark:` classes and a toggle.
- **Done when:** the whole app is usable at 390 px width.

Also in V1 gaps for you: the complete tick on the card, the list "⋯" menu, the hover quick-menu on a card (see wireframe, dashed "V1" markers).

---

## Person 4 (Ali): Database + JavaScript (and Project Manager)

Files: `db.py`, `SCHEMA.md`, `static/js/*.js`. Warm-up: Part 4.

### A1. New schema and migration
- **Why:** everyone's code depends on the data shapes (section 0.1).
- **Where:** `SCHEMA.md`, a one-time script `migrate_v2.py`.
- **Steps:** update `SCHEMA.md`; write a script that turns each old board's `owner_id` into `members: [{"user_id": owner_id, "role": "owner"}]`, and adds `checklist: []`, `comments: []`, `activity: []`, `completed: False` to old cards.
- **Done when:** the old data still loads and `SCHEMA.md` is merged first (the others wait for it).

### A2. Database helper functions
- **Why:** so the backend people do not each write their own queries.
- **Where:** `db.py`.
- **Build:** `toggle_checklist_item`, `add_comment_db`, `boards_for_user` (see Part 4 of the warm-up). Document each helper with a short docstring.

### A3. JavaScript: checklist, comments, dialog
- **Where:** `static/js/card_dialog.js` (new file; confirm with the PM because it changes the structure).
- **Build:** `openCard(id)` fills the dialog from `/card/<id>/json`; tick/add/delete a checklist item and update the bar and badge without reloading; send a comment and add the bubble.
- **Depends on:** P2-1, P2-2, P2-3 and Mamur's ids.

### A4. JavaScript: live filter and drag-and-drop keeps working
- **Where:** `static/js/filter.js`, `static/js/drag_drop.js`.
- **Build:** the live text filter (pure JS); member/label/due filters call P2-4; make sure moving a card still saves after the new layout.

### PM duties (Ali)
- Create GitHub Issues for every task above with the template in this file, and a Project board.
- Review each Pull Request within 24 hours; merge in this order: A1, P1-1, P1-2, then the rest.
- Run the full test at the end (see below).

---

## Issue template (copy into `.github/ISSUE_TEMPLATE/task.md`)

```
Title: [V2][Role] short action

Owner:
Branch:
Depends on:

What to build:
-

Where (files):

Done when:
- [ ]
- [ ] PR opened and reviewed
```

## Final test (Definition of Done for V2)
- [ ] Register user A and user B. User A creates a board. User B cannot open it (403).
- [ ] A invites B by email. B sees the board on the dashboard and can add cards.
- [ ] B (member) does not see the Share form and cannot remove anyone.
- [ ] Checklist: add 5 items, tick 2, the badge shows 2/5 and the bar shows 40 percent.
- [ ] Comment and activity: a comment appears first, moving a card adds an activity line.
- [ ] Filter by text, member, label, due date, and Clear filters.
- [ ] Usable on a phone width (390 px). `.env` is not in `git status`.
