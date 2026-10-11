# 📋 Tarmo — Project 3 (Flask + MongoDB)

Our third team practice project. A simplified Trello-style task board: boards,
lists (columns), and cards you can create, move, label, assign, and comment on.
Built to practice **Python (Flask)**, **MongoDB**, **basic frontend (HTML/CSS/JS)**,
and professional coding standards (environment secrets, password hashing,
middleware) as a team.

---

## ⚠️ Before You Start: Practice First

Do the warm-up notebook for your role before touching the real code:
- **Person 1 & Person 2 (Python/Flask):** `Backend_Warmup_Trello_Project.ipynb`
- **Person 3 (HTML/CSS):** warm-up notebook to follow
- **Person 4 (Database + JS):** warm-up notebook to follow

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask |
| Database | MongoDB (Atlas, free tier) |
| Frontend | HTML + Tailwind CSS |
| Interactivity | JavaScript (SortableJS for drag-and-drop) |
| Auth | Flask session + Werkzeug password hashing |
| Secrets | `.env` file (python-dotenv) |

---

## 🗂️ Project Structure

```
trello-clone/
├── app.py                          # Flask entry point (pre-built, shared)
├── db.py                             # MongoDB connection (Person 4)
├── SCHEMA.md                           # MongoDB collection shapes (Person 4)
├── auth/
│   ├── decorators.py                     # login_required / admin_required middleware (pre-built)
│   └── routes.py                           # register / login / logout (Person 1)
├── routes/
│   ├── boards.py                             # boards, lists, dashboard (Person 1)
│   ├── cards.py                                # cards: create/move/edit/delete (Person 2)
│   ├── card_details.py                           # labels, due dates, assign, comments (Person 2)
│   └── search_archive_reports.py                   # search, archive, stats (Person 2)
├── templates/                                        # Jinja/HTML pages (Person 3 — currently placeholders)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── board.html
├── static/
│   ├── css/style.css                                   # styling (Person 3 — currently placeholder)
│   └── js/drag_drop.js                                   # drag-and-drop (Person 4 — currently placeholder)
├── .env.example                                            # template for secrets (copy to .env, never commit .env)
├── .gitignore
├── requirements.txt
└── README.md
```

### How the pieces connect
```
Browser
   │
   ▼
app.py  (registers everyone's routes as Blueprints)
   │
   ├── auth/routes.py        ──┐
   ├── routes/boards.py        ├── all call db.py to read/write MongoDB
   ├── routes/cards.py         │
   ├── routes/card_details.py  │
   └── routes/search_...py   ──┘
   │
   ▼
templates/*.html  (Jinja renders data into Person 3's HTML/Tailwind pages)
   │
   ▼
static/js/drag_drop.js  (calls routes/cards.py's /card/<id>/move endpoint)
```

---

## 🔐 Standards Used in This Project

**1. Secrets live in `.env`, never in code**
Copy `.env.example` to `.env` and fill in real values. `.env` is in `.gitignore`
— it must never be committed or pushed to GitHub. Every secret (database
connection string, Flask secret key) is read with `os.environ.get(...)`.

**2. Passwords are always hashed**
`auth/routes.py` uses `werkzeug.security.generate_password_hash()` when
registering and `check_password_hash()` when logging in. Plain-text
passwords are never stored anywhere.

**3. Middleware protects routes**
`auth/decorators.py` provides `@login_required` and `@admin_required`,
applied to any route that shouldn't be open to everyone (see `routes/boards.py`
for examples of both).

---

## 🛢️ Database Setup (Person 4)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) and create a free account
2. Create a **Free Cluster** (M0 tier)
3. Create a Database User (username + password)
4. Under Network Access, allow access from anywhere (`0.0.0.0/0`) so every
   teammate can connect while developing
5. Copy the connection string (**Connect → Drivers**) — looks like:
   `mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/`
6. Copy `.env.example` to `.env` and paste it into `MONGO_URI`
7. Test the connection:
   ```bash
   python db.py
   ```
   You should see `Connected successfully to database: trello_clone`

Collection shapes are documented in `SCHEMA.md` — refine it as fields get finalized.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
cp .env.example .env     # then fill in real MONGO_URI and SECRET_KEY
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 👥 Team Assignments

| Person | Role | Files | Tasks |
|---|---|---|---|
| **Person 1** | Backend (Python) | `auth/routes.py`, `routes/boards.py` | Register/login/logout, boards, lists, dashboard |
| **Person 2** | Backend (Python) | `routes/cards.py`, `routes/card_details.py`, `routes/search_archive_reports.py` | Cards, labels/due dates/assign/comments, search/archive/stats |
| **Person 3** | Frontend (HTML/CSS) | `templates/*.html`, `static/css/style.css` | Replace placeholder templates with real Tailwind design |
| **Person 4** | Database + JS | `db.py`, `SCHEMA.md`, `static/js/drag_drop.js` | MongoDB Atlas setup, schema, drag-and-drop with SortableJS |

Every backend function has a `TODO` docstring with exact steps — follow the
`load → change → save/return` pattern from the warm-up notebook and the
Library project.

---

## 🔀 Git Workflow

Same as previous projects:

1. `git clone <repo-url>` (first time only)
2. `git checkout main && git pull origin main` (before starting new work)
3. `git checkout -b yourname-task`
4. Write code, test locally
5. `git add . && git commit -m "..."`
6. `git push origin yourname-task`
7. Open a Pull Request → review → merge into `main`
8. `git pull origin main` before your next task

> **Never commit `.env`.** It's already in `.gitignore`, but double-check
> before every push — a leaked database password means recreating the whole
> Atlas cluster from scratch.

---

## ✅ Definition of Done

- [ ] Everyone completed their role's warm-up notebook
- [ ] MongoDB Atlas cluster set up and `python db.py` connects successfully
- [ ] Person 1: register, login, logout, boards, and lists all work
- [ ] Person 2: cards, card details, search, archive, and stats all work
- [ ] Person 3: real Tailwind design replaces all placeholder templates
- [ ] Person 4: drag-and-drop moves cards between lists and saves to MongoDB
- [ ] `.env` never appears in `git status` as a tracked file
- [ ] Full flow works end-to-end: register → login → create board → add
      lists → add cards → label/assign/comment → drag between lists → search
      → archive → view stats

---

## ℹ️ Note

This project is designed for learning and practice, planned and maintained by
the Project Manager. Any change to this README's text or structure, or to
the project's file structure, or any push/upload to the shared repo, should
be confirmed with the Project Manager first.


V2: see docs/v2/TASKS.md
