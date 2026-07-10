# Backend (Student 1) — Beginner's Step-by-Step Guide
### For your 7-Day Sprint: Auth, Session/Interval Logic, Rule Engine, Export

This guide assumes you've never coded a backend before. Follow it top to bottom, in order — don't skip to Day 3 code before Day 1 setup works. A starter project (`main.py`, `auth.py`, `logic.py`, `database.py`, `requirements.txt`) is attached alongside this guide — you can run it as-is and modify it as you go.

---

## Step 1: Software Installation

Install these three things, in this order. Use a **Mac or Windows laptop** (not a tablet/Chromebook) — you need a real terminal.

### 1. Python
- Download: **https://www.python.org/downloads/** (get the latest 3.11 or 3.12 version)
- **Windows:** during install, check the box **"Add python.exe to PATH"** before clicking Install — this is the single most common beginner mistake, so don't miss it.
- **Mac:** run the downloaded `.pkg` installer normally.

**Verify it worked** — open your terminal (Windows: search "Command Prompt" or "PowerShell"; Mac: search "Terminal") and type:
```bash
python --version
```
If that fails on Mac, try:
```bash
python3 --version
```
You should see something like `Python 3.11.6`. If you see an error instead, close and reopen your terminal, or reinstall checking the PATH box.

### 2. VS Code (your code editor)
- Download: **https://code.visualstudio.com/**
- Install with default options.
- Open VS Code, go to the Extensions icon on the left sidebar (four squares), and install **"Python"** (by Microsoft).

### 3. Git (for version control / GitHub)
- Download: **https://git-scm.com/downloads**
- Install with default options (just keep clicking Next).

**Verify it worked** — in your terminal:
```bash
git --version
```
You should see something like `git version 2.43.0`.

### 4. A GitHub account
- Go to **https://github.com** and sign up if you don't already have an account (free).

Once all three commands above return a version number instead of an error, you're ready for Step 2.

---

## Step 2: Day 1 — API Contract Setup

### 2.1 Create your project folder
In your terminal:
```bash
cd Desktop
mkdir attendance-backend
cd attendance-backend
```

### 2.2 Create a virtual environment (keeps this project's packages separate from everything else on your computer)
```bash
python -m venv venv
```
Activate it:
- **Windows (PowerShell):** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

You'll know it worked because your terminal prompt now shows `(venv)` at the start of the line. **You need to run this activate command every time you open a new terminal to work on this project.**

### 2.3 Install FastAPI and friends
Copy the attached `requirements.txt` file into this folder, then run:
```bash
pip install -r requirements.txt
```

### 2.4 Copy in the starter files
Copy `main.py`, `auth.py`, `logic.py`, and `database.py` (all attached) into your `attendance-backend` folder. Your folder should now look like:
```
attendance-backend/
├── venv/
├── requirements.txt
├── main.py
├── auth.py
├── logic.py
└── database.py
```

### 2.5 Run your server
```bash
uvicorn main:app --reload
```
You should see output ending in something like:
```
Uvicorn running on http://127.0.0.1:8000
```
Leave this terminal window running — this is your live server.

### 2.6 Find your Interactive Docs (Swagger UI) — this is your API contract
Open a browser and go to:
```
http://127.0.0.1:8000/docs
```
This page **is** your API contract. It's auto-generated from your code — every endpoint, its inputs, and its outputs are listed there, and your teammates can even try calling your API directly from that page.

**This is the single most important thing to do on Day 1.** Send your Frontend and ML teammates:
1. A screenshot or screen-share of this `/docs` page, **and**
2. The plan: once your code is on GitHub (Step 5), they can run it themselves and see the same page on their own laptop at the same URL.

If this page loads and shows endpoints like `/health`, `/stub-vector`, `/signup`, `/login` — you're done with Day 1.

---

## Step 3: Writing the Core Logic

You don't need to write these from scratch — they're in the attached starter files — but you do need to understand them, because you'll be extending them daily and explaining them if asked.

### Auth (`auth.py` + parts of `main.py`)
The pattern is always the same three steps:
1. **Signup:** hash the password (never store it as plain text), save the user.
2. **Login:** check the submitted password against the stored hash; if it matches, issue a **JWT** — a signed token that says "this is user #7, role Teacher, valid for 2 hours."
3. **Every protected endpoint:** reads that token from the request, decodes it, and checks the role before doing anything.

```python
# The core idea, simplified:
token = create_access_token(user_id=user.user_id, role=user.role)
# ...later, on a protected endpoint:
payload = decode_access_token(token)   # raises an error if invalid/expired
```

### Session/Interval Logic (`logic.py`)
This is a **pure function** — no database, no FastAPI, just math. That's deliberate: it's the easiest thing on your whole backlog to test in isolation.

```python
def calculate_intervals(session_duration_minutes, max_snapshots=6, min_gap_minutes=5):
    snapshot_count = max_snapshots
    interval_minutes = session_duration_minutes / snapshot_count
    while interval_minutes < min_gap_minutes and snapshot_count > 1:
        snapshot_count -= 1
        interval_minutes = session_duration_minutes / snapshot_count
    return snapshot_count, round(interval_minutes, 2)
```
Worked examples this must match (from your architecture doc):
| Input | Expected Output |
|---|---|
| 50 minutes | 6 snapshots, ~8.33 min apart |
| 90 minutes | 6 snapshots, 15 min apart |
| 20 minutes | 4 snapshots, 5 min apart |

### Rule Engine (`logic.py`)
Also a pure function — takes a count, returns a status:
```python
def determine_attendance_status(scan_matches):
    if scan_matches >= 5:
        return "Present"
    elif scan_matches >= 3:
        return "Pending_Review"
    else:
        return "Absent"
```

---

## Step 4: How to Execute & Test

### Run the server
```bash
uvicorn main:app --reload
```
`--reload` means the server automatically restarts whenever you save a code change — keep this on while developing.

### Test the pure logic functions directly (fastest way to check Day 3/5 work)
```bash
python logic.py
```
This runs the built-in test block at the bottom of `logic.py` and prints whether your interval math matches the worked examples above.

### Test your API endpoints via Swagger UI (easiest for beginners)
1. Go to `http://127.0.0.1:8000/docs`
2. Click on an endpoint, e.g. `POST /signup`
3. Click **"Try it out"**
4. Fill in the example JSON (change values as needed)
5. Click **"Execute"** — you'll see the real response below, including the HTTP status code

**Suggested test order** (matches your endpoints in `main.py`):
1. `GET /health` → should return `{"status": "ok"}`
2. `POST /signup` → create a Teacher and a Student and an Admin (do this 3 times with different emails/roles)
3. `POST /login` → note: this form asks for "username" — put the **email** there. Copy the `access_token` you get back.
4. Click the green **"Authorize"** button at the top of the `/docs` page, paste in `Bearer <your_token>`, and now your protected endpoints (like `/pending-registrations`) will work when you try them.
5. `POST /stub-vector` → confirms your fake face-vector generator works
6. `POST /register-face`, then `GET /pending-registrations` (as Admin), then `POST /approve-registration/{id}`
7. `POST /sessions` (as Teacher) → try `session_duration_minutes: 50` and confirm you get back `snapshot_count: 6, interval_minutes: 8.33`

### Test via terminal instead of Swagger (optional, once comfortable)
```bash
curl http://127.0.0.1:8000/health
```

---

## Step 5: Git & Daily Commits

Do this once, on Day 1, right after your server runs successfully.

### 5.1 Create the GitHub repo
- Go to github.com → click the **+** icon top-right → **New repository**
- Name it e.g. `attendance-tracker-backend`
- Leave it **empty** (don't check "add README") — you'll push your existing code into it
- Click **Create repository** and keep the page open — it shows you the commands you need (similar to below)

### 5.2 Initialize Git locally and push for the first time
In your terminal, inside `attendance-backend/`:
```bash
git init
```
Create a file called `.gitignore` (so you don't accidentally upload your virtual environment or database file) with this content:
```
venv/
__pycache__/
*.db
.env
```
Then:
```bash
git add .
git commit -m "Day 1: FastAPI skeleton, stub vector endpoint, health check"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/attendance-tracker-backend.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your actual GitHub username — you'll find the exact URL on the GitHub page from step 5.1.

### 5.3 Your daily commit routine (Days 2–7)
Every day, after you've made progress:
```bash
git add .
git commit -m "Day 2: JWT auth, signup/login endpoints"
git push
```
**Match your commit messages to the day and feature**, e.g.:
- Day 2: `"Day 2: JWT auth, signup/login endpoints"`
- Day 3: `"Day 3: session creation endpoint + interval calculation"`
- Day 4: `"Day 4: scan-result endpoint wired to matching"`
- Day 5: `"Day 5: rule engine + finalize-attendance endpoint"`
- Day 6: `"Day 6: export endpoint"`
- Day 7: `"Day 7: integration fixes"` (commit multiple times today as you fix bugs)

This is what creates the **daily commit trail across all 7 days** your grading rubric asks for — commit at the end of every single working session, even small ones. A commit that's just "fixed a typo" is fine; an empty day with no commits is the thing to avoid.

### 5.4 If you get a merge conflict
Per your sprint's Git plan: pull before you push, and if you can't resolve a conflict within 10 minutes, stop and call your teammates instead of struggling alone.
```bash
git pull origin main
# fix any conflicts VS Code highlights for you, then:
git add .
git commit -m "resolve merge conflict"
git push
```

---

## Quick Reference: Your Daily Checklist
- [ ] `cd attendance-backend` then activate venv (`source venv/bin/activate` or `venv\Scripts\activate`)
- [ ] `uvicorn main:app --reload` to run the server
- [ ] Test your new endpoint(s) at `http://127.0.0.1:8000/docs`
- [ ] `git add .` → `git commit -m "Day N: ..."` → `git push`
