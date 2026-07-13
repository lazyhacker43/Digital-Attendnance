# Student 2 (Frontend) — Beginner's 7-Day Survival Guide
### Snapshot Attendance Tracker — Sprint Plan

Stack: **HTML + CSS + JavaScript (vanilla)** — no framework, no build step, nothing to configure. You write a file, you open it, it works.

---

## Step 1 — Software Installation

Download these four things. All free, all official links.

1. **VS Code** (code editor) — https://code.visualstudio.com/
   - Download for your OS, run the installer, accept defaults, launch it.

2. **Git** (for your daily commits) — https://git-scm.com/downloads
   - Windows: run the installer, accept all defaults (just keep clicking "Next").
   - Mac: easiest is opening Terminal and typing `git --version` — if it's not installed, macOS will prompt you to install Xcode Command Line Tools, click yes.

3. **Node.js** (LTS version) — https://nodejs.org/
   - You don't strictly need this for plain HTML/CSS/JS, but you'll want it on Day 6–7 to deploy to Vercel easily. Install the **LTS** version, accept defaults.

4. **VS Code "Live Server" extension**
   - Open VS Code → click the Extensions icon (four squares) on the left sidebar → search "Live Server" (by Ritwick Dey) → click Install.
   - This lets you right-click any HTML file and choose "Open with Live Server" — it auto-refreshes your browser every time you save. This is how you'll preview your work all week.

5. **A free GitHub account** (if you don't have one) — https://github.com/join
   - Create a repository for the project (or your teammates create it and add you as a collaborator — coordinate this on Day 1 standup).

That's it. No Python, no npm installs required to get started.

---

## Step 2 — Project Setup

Create a folder structure like this:

```
snapshot-attendance-frontend/
├── index.html          ← Login page
├── admin.html           ← Admin dashboard
├── teacher.html          ← Teacher dashboard
├── student.html          ← Student dashboard
├── css/
│   └── style.css
├── js/
│   ├── api.js            ← all your fetch() calls live here
│   └── app.js             ← page-specific interactivity
└── README.md
```

How to create it:
1. Make a new folder on your computer named `snapshot-attendance-frontend`.
2. Open VS Code → File → Open Folder → select it.
3. In VS Code's file explorer (left sidebar), click the "New File" icon and type `index.html`. Do the same for the others. Right-click the folder area to create the `css/` and `js/` subfolders first, then create files inside them.

You now have a real project skeleton. This matches the same route structure your teammates expect (Admin / Teacher / Student), just as separate HTML pages instead of Next.js routes — functionally identical for a 1-week MVP.

---

## Step 3 — Creating the UI Components

I've built you three starter files (attached separately, ready to open): `index.html`, `style.css`, and `script.js`. They include:

- A **dropdown for interval selection** (50-min / 90-min, matching Student 1's session logic)
- A **visual alert container** that changes color (green/yellow/red) based on attendance thresholds from the rule engine (5–6 / 3–4 / 0–2)
- A **functional export button**
- **Error message handling** for bad/missing data
- Clean, aligned layout using CSS Flexbox/Grid — no framework needed

Open `index.html` with Live Server right now to see it render. Then copy the same `<head>`/CSS link pattern into your other pages (`admin.html`, `teacher.html`, `student.html`) as you build them out day by day.

Key patterns worth understanding (don't just copy-paste blindly — this is what you'll be extending all week):

```html
<!-- Interval picker -->
<select id="intervalPicker">
  <option value="50">50-minute session</option>
  <option value="90">90-minute session</option>
</select>
```

```css
/* Alert states — JS just toggles these classes */
.alert-box { padding: 16px; border-radius: 8px; font-weight: 600; }
.alert-green  { background: #d1fae5; color: #065f46; }
.alert-yellow { background: #fef3c7; color: #92400e; }
.alert-red    { background: #fee2e2; color: #991b1b; }
```

```js
function setAlertLevel(status) {
  const box = document.getElementById('alertBox');
  box.className = 'alert-box'; // reset
  if (status === 'present')  box.classList.add('alert-green');
  if (status === 'partial')  box.classList.add('alert-yellow');
  if (status === 'absent')   box.classList.add('alert-red');
}
```

---

## Step 4 — Connecting to the Backend

On **Day 2**, Student 1 will publish the API schema. Read it carefully and note the exact endpoint URLs, expected JSON shape, and auth requirements (JWT token in headers). Ask questions in standup immediately if anything is unclear — don't guess.

Here's the exact pattern you'll use everywhere. Put this in `js/api.js`:

```js
const API_BASE = "http://localhost:8000"; // swap for the deployed Render/Railway URL later

async function fetchSessionStatus(sessionId) {
  try {
    const response = await fetch(`${API_BASE}/sessions/${sessionId}/status`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`Server responded with ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    showError("Could not load session data. Please try again.");
    console.error(error);
    return null;
  }
}

function showError(message) {
  const errorBox = document.getElementById('errorBox');
  errorBox.textContent = message;
  errorBox.style.display = 'block';
}
```

Sending data (e.g. the interval a Teacher picks) works the same way with `method: "POST"` and a `body`:

```js
async function createSession(intervalMinutes) {
  try {
    const response = await fetch(`${API_BASE}/sessions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ interval_minutes: intervalMinutes })
    });

    if (!response.ok) throw new Error(`Server responded with ${response.status}`);
    return await response.json();

  } catch (error) {
    showError("Could not start session. Check your connection and try again.");
    console.error(error);
  }
}
```

**Until Day 2**, you won't have a real backend to call — that's expected and by design (see your plan's Section 1: "Student 2 can build the entire UI against a mocked API from Day 1"). Fake it like this:

```js
// mock-data.js — delete this file once real backend is live
function mockSessionStatus() {
  return Promise.resolve({
    session_id: 1,
    students: [
      { name: "Asha K.", status: "present" },
      { name: "Rohan T.", status: "partial" },
      { name: "Priya S.", status: "absent" }
    ]
  });
}
```

Call `mockSessionStatus()` instead of `fetchSessionStatus()` in your early UI code, then swap the function name once the real API is ready on Day 2. This is exactly how your teammates expect you to work.

---

## Step 5 — Git & Daily Commits (secures your 20% weight)

Run these **once**, on Day 1, in your project folder (open VS Code's terminal: Terminal → New Terminal):

```bash
git init
git remote add origin <the-repo-url-your-team-created>
git checkout -b student2
```

Then, **every single day** (do this at minimum once, ideally twice — matching your team's "merge to main at least twice a day" rule):

```bash
git add .
git commit -m "Day 1: HTML skeleton, routing, mock API wiring"
git push origin student2
```

Change the commit message each day to reflect real progress, e.g.:
- Day 1: `"Day 1: page skeletons + mock data wiring"`
- Day 2: `"Day 2: Login UI + Admin dashboard wired to real backend"`
- Day 3: `"Day 3: registration page with camera capture"`
- Day 4: `"Day 4: Teacher dashboard live scan progress view"`
- Day 5: `"Day 5: client-side scan trigger + review UI"`
- Day 6: `"Day 6: Student dashboard + bug fixes from Day 5"`
- Day 7: `"Day 7: integration fixes + Vercel deploy"`

Before each merge into `main`, pull the latest changes first so you don't clobber your teammates:

```bash
git checkout main
git pull origin main
git checkout student2
git merge main
# resolve any conflicts in VS Code if prompted
git push origin student2
```

Then open a quick merge/PR into `main` (or merge directly if your team agreed to skip PRs — your plan allows this for a 1-week sprint). This visible daily trail on your own branch is exactly what satisfies the "Daily commit trail" 20% criterion — commit *something* every day even if it's small, don't cluster it all at the end.

---

## Day-by-Day Checklist (mapped to your actual sprint plan)

| Day | What you build | Commit by end of day |
|---|---|---|
| 1 | HTML skeletons for all 4 pages, CSS base styles, mock API responses | ✅ |
| 2 | Login UI + Admin dashboard (Pending list, Approve button) wired to **real** backend once Student 1 publishes schema | ✅ |
| 3 | Registration page with real camera capture (`getUserMedia`) | ✅ |
| 4 | Teacher dashboard: start session, live scan progress view | ✅ |
| 5 | Client-side scan trigger (`setInterval` synced to schedule) + Teacher review UI (Pending toggle) | ✅ |
| 6 | Student dashboard (view own attendance) + fix bugs flagged Day 5 | ✅ |
| 7 | **No new features.** Integration test with the whole team, fix cross-role bugs, deploy to Vercel, rehearse demo | ✅ |

A quick note on Day 7 deploy: once Node.js is installed, deploying a plain HTML/CSS/JS site to Vercel is just:
```bash
npm install -g vercel
vercel
```
Follow the prompts (link to your project folder), and it gives you a live URL in under a minute.

You've got everything you need to start today. Good luck.
