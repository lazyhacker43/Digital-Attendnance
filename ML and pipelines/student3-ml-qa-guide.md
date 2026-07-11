# Student 3 (ML / QA / DevOps) — Beginner's 7-Day Survival Guide
### Snapshot Attendance Tracker — Sprint Plan

Stack: **Python** for the ML/QA logic, **pytest** for tests, **GitHub Actions** for CI. All free, all standard, all beginner-reachable in a week.

---

## Step 1 — Software Installation

1. **Python 3.11+** — https://www.python.org/downloads/
   - Windows: run the installer. **Critical**: check the box "Add python.exe to PATH" before clicking Install — this is the #1 thing beginners miss.
   - Mac: download the macOS installer from the same page and run it.
   - Verify it worked: open a terminal (Terminal on Mac, Command Prompt or PowerShell on Windows) and type:
     ```bash
     python --version
     ```
     You should see `Python 3.11.x` or similar. (On Mac it may be `python3 --version` instead.)

2. **VS Code** — https://code.visualstudio.com/
   - Install it, then open Extensions (four-squares icon) → search "Python" (by Microsoft) → Install. This gives you a "Run" button and test discovery inside VS Code.

3. **Git** — https://git-scm.com/downloads
   - Accept defaults during install. Verify with `git --version` in your terminal.

4. **A free GitHub account** (if you don't have one) — https://github.com/join
   - You'll need this for both your daily commits and GitHub Actions (CI runs on GitHub's servers automatically, free for public repos and free-tier for private ones on personal accounts).

Once those three are installed, set up your project:

```bash
mkdir snapshot-attendance-ml
cd snapshot-attendance-ml
python -m venv venv
```

Activate the virtual environment (do this every time you open a new terminal to work on this project):
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Then install your starting dependencies:
```bash
pip install pytest numpy pandas
```

Note on `face_recognition`/`dlib`: that library requires a C++ compiler (`cmake`) to install and can be genuinely painful to set up on Windows. Don't install it on Day 1 — get your mock pipeline and tests working first (Steps 2–3 below), then tackle the real encoding install on Day 2 when your actual sprint task calls for it. If it fights you, `pip install face_recognition` on Mac usually needs `brew install cmake` first; on Windows, install "Desktop development with C++" via the Visual Studio Build Tools installer before retrying pip.

---

## Step 2 — Day 1–3: Mock ML / Validation Script

Your plan requires you to unblock Student 1 and Student 2 by Day 3 with a mock prediction data structure — something that returns realistic-shaped fake data so they can build against it without waiting for your real face-matching pipeline.

Create `mock_face_match.py`:

```python
"""
Mock face-matching module.
Returns data in the SAME SHAPE the real pipeline will eventually return,
so Student 1 (backend) and Student 2 (frontend) can build against this
immediately instead of waiting for real ML.

Swap calls to this module for the real one once Day 2's real encoding is live.
"""

import random

def mock_encode_face(image_bytes=None):
    """Pretend to turn a camera frame into a 128-d face embedding."""
    return [round(random.uniform(-1, 1), 4) for _ in range(128)]


def mock_match_face(embedding, known_embeddings, threshold=0.6):
    """
    Pretend to compare an embedding against known students.
    Returns a fake match result in the real pipeline's expected shape.
    """
    if not known_embeddings:
        return {"matched": False, "student_id": None, "confidence": 0.0}

    # Randomly "match" one of the known students for testing purposes
    matched_student = random.choice(list(known_embeddings.keys()))
    fake_confidence = round(random.uniform(threshold, 1.0), 3)

    return {
        "matched": True,
        "student_id": matched_student,
        "confidence": fake_confidence
    }


if __name__ == "__main__":
    # Quick manual check — run this file directly to see sample output
    known = {"student_101": [0.1] * 128, "student_102": [0.2] * 128}
    fake_embedding = mock_encode_face()
    result = mock_match_face(fake_embedding, known)
    print("Encoded embedding (first 5 values):", fake_embedding[:5])
    print("Match result:", result)
```

Run it to confirm it works:
```bash
python mock_face_match.py
```

Share this file (and the exact shape of `mock_match_face`'s return dict) with Student 1 and Student 2 in your Day 1–2 standup — that dict shape is the "contract" they'll build their UI and endpoint around, same as Student 1's API schema is a contract for everyone else.

---

## Step 3 — Writing Automated Tests (QA)

You'll use `pytest` — simpler syntax than `unittest`, and it's what most real teams use.

First, here's a standalone reference implementation of the **rule engine** (5–6 → present, 3–4 → partial, 0–2 → absent) so you can test threshold logic independently, before Student 1's real backend endpoint exists. Once Student 1's real endpoint is live (Day 5), you'll test against theirs instead — but having your own copy lets you write and validate tests from Day 1 without being blocked.

Create `rule_engine.py`:

```python
"""
Reference implementation of the attendance rule engine.
Thresholds (out of a max of 6 scan intervals per session):
  5-6 intervals matched -> "present"
  3-4 intervals matched -> "partial"
  0-2 intervals matched -> "absent"
"""

def classify_attendance(intervals_present: int, total_intervals: int = 6) -> str:
    if intervals_present < 0 or intervals_present > total_intervals:
        raise ValueError(f"intervals_present must be between 0 and {total_intervals}")

    if intervals_present >= 5:
        return "present"
    elif intervals_present >= 3:
        return "partial"
    else:
        return "absent"
```

Now create `test_rule_engine.py`:

```python
import pytest
from rule_engine import classify_attendance

def test_full_attendance_is_present():
    assert classify_attendance(6) == "present"

def test_five_intervals_is_present():
    assert classify_attendance(5) == "present"

def test_four_intervals_is_partial():
    assert classify_attendance(4) == "partial"

def test_three_intervals_is_partial():
    assert classify_attendance(3) == "partial"

def test_two_intervals_is_absent():
    assert classify_attendance(2) == "absent"

def test_zero_intervals_is_absent():
    assert classify_attendance(0) == "absent"

def test_negative_intervals_raises_error():
    with pytest.raises(ValueError):
        classify_attendance(-1)

def test_over_max_intervals_raises_error():
    with pytest.raises(ValueError):
        classify_attendance(7)

def test_mock_match_returns_expected_shape():
    from mock_face_match import mock_match_face
    known = {"student_101": [0.1] * 128}
    result = mock_match_face([0.0] * 128, known)
    assert "matched" in result
    assert "student_id" in result
    assert "confidence" in result
```

Run your tests:
```bash
pytest -v
```

You should see 9 tests pass with green checkmarks. This is exactly what "Correctness of core logic" (20% of your grade) is checking for — boundary cases (2 vs 3, 4 vs 5) matter more than volume of tests, so don't pad this with dozens of near-duplicate tests. A handful of well-chosen edge cases beats fifty redundant ones.

On **Day 5**, when Student 1's real rule engine endpoint is live, add an integration test that calls their real endpoint (via `requests`) with mock session data and checks the same thresholds hold end-to-end — that's your "mock-session integration test" from the plan.

---

## Step 4 — Setting Up the Pipeline (GitHub Actions CI)

This makes your tests run automatically every time anyone pushes code — no manual "did I remember to run the tests" step.

In your project folder, create this exact path: `.github/workflows/ci.yml`

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml`:

```yaml
name: CI - Run Tests

on:
  push:
    branches: [ main, student3 ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest numpy pandas

      - name: Run tests
        run: pytest -v
```

Also create a `requirements.txt` in your project root so the CI (and your teammates) can install exactly what you use:
```
pytest
numpy
pandas
```

Push this to GitHub, then go to your repo's **Actions** tab — you'll see the workflow run automatically and show a green checkmark (or a red X telling you exactly which test failed). This is your functioning CI/CD deliverable: real, automatic, and something you can point to and demo on Day 7 without having spent three days building it.

---

## Step 5 — Git & Daily Commits (secures your 20% weight)

Run these **once**, on Day 1:

```bash
git init
git remote add origin <the-repo-url-your-team-created>
git checkout -b student3
git add .
git commit -m "Day 1: local face_recognition setup, mock encoding module, webcam test"
git push origin student3
```

Then, **every day** for the rest of the sprint:

```bash
git add .
git commit -m "Day X: <what you actually did>"
git push origin student3
```

Suggested daily messages matching your actual sprint tasks:
- Day 1: `"Day 1: mock face-match module + webcam isolation test"`
- Day 2: `"Day 2: real encoding swapped in for stub; confirmed no frame persists to disk"`
- Day 3: `"Day 3: matching logic vs Biometric_Embeddings, default threshold"`
- Day 4: `"Day 4: integration test with mock multi-face frames; logged false accepts/rejects"`
- Day 5: `"Day 5: full mock session test against live rule engine; bug log updated"`
- Day 6: `"Day 6: pandas/openpyxl export function + backend deploy to Render"`
- Day 7: `"Day 7: end-to-end dry run fixes, deploy verification, CI green"`

Before merging into `main`, pull first to avoid clobbering teammates:
```bash
git checkout main
git pull origin main
git checkout student3
git merge main
# resolve conflicts in VS Code if prompted
git push origin student3
```

This gives you a visible daily trail on your own branch — exactly what the "Daily commit trail" criterion checks for. Commit something real every day, even if small; don't cluster it all at the end.

---

## Day-by-Day Checklist (mapped to your actual sprint plan)

| Day | What you build | Commit by end of day |
|---|---|---|
| 1 | `face_recognition`/dlib environment set up locally; mock match module; webcam isolation test | ✅ |
| 2 | Swap stub for real encoding; confirm frames never persist to disk (log proof of this — screenshot or log line) | ✅ |
| 3 | Matching logic: Euclidean distance vs. known embeddings, library default threshold — **and share the mock data contract with the team if not already done** | ✅ |
| 4 | Integration-test matching with mock multi-face frames; flag false accepts/rejects in a shared bug log | ✅ |
| 5 | Run full mock session (varied attendance) against the live rule engine; log results | ✅ |
| 6 | Pandas/OpenPyXL export function, spot-checked by hand; deploy backend to Render/Railway | ✅ |
| 7 | Full end-to-end dry run with the team; fix cross-role bugs; confirm deploy talks to frontend; CI green | ✅ |

You've got a real, working pipeline scaffold to start from today — good luck.
