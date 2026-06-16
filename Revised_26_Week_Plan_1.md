# Revised 26-Week Plan — Job-Ready in 6 Months

## How this plan differs from the original

The original plan assumed 2-hour sessions and 112 days of content.
Your actual pace is 3–6 hours per session. This plan works with that.

**Unit = one session (target 3–4 hours, accept 2–6).**
Plan contains ~60 sessions across 26 weeks = roughly 4–5 sessions per week.
At 3 sessions per week you finish in time. At 5 you have buffer for life.

**Three rules that replace ten:**
1. Git commit at the end of every session. No exceptions.
2. Every project gets a README written *while you build*, not after.
3. Before touching old code after a break, read your README first. This solves the re-entry problem.

**What was cut and why:**
- Desktop app rebuild (Tkinter is not a hiring skill — drop it entirely)
- Week 10–11 desktop section replaced with deeper Flask/portfolio time
- Abstract "Task class" OOP exercises replaced with Genshin character as the domain (you already know it)
- Planning week compressed from 7 sessions to 2

**What was added:**
- "Rebuild from memory" sessions explicitly scheduled — this is the core fix for your internalization problem
- Git introduced session 1, not week 2
- Each phase ends with a spoken self-test prompt

---

## Phase 1 — Python Re-anchor and Git Foundation
### Sessions 1–10 | Weeks 1–2

**Goal:** Prove you can write clean modular Python from memory and commit it properly.
You are currently here. Complete this phase before moving on.

---

### Session 1: Finish Week 1 foundations + Git local setup
**Build:** Complete Day 6 work (`safe_division.py`, `file_reader.py`, `retry_number_input.py`).
**Also:** `git init` your practice folder. Make your first real commit. Write a 3-line README.
**Done means:** Exceptions are caught specifically (not bare `except`). You made at least 3 commits with real messages. You can explain what `.gitignore` is for.
**Self-test:** Close everything. Open a terminal. Where is your repo? What is the last thing you committed?

---

### Session 2: Week 1 checkpoint — tracker app
**Build:** `week1_tracker.py` — add/view/remove/count/exit, no crashes on bad input, no blank items.
**Done means:** You wrote the menu loop without looking at your `menu_utils.py`. You committed a stable version.
**Self-test:** Can you explain `nonlocal` out loud without reading your code?

---

### Session 3: Dictionaries, files, JSON
**Build:** `contact_book.py` — list of dicts, JSON save/load, first-run safe, corrupt-file safe.
**Done means:** Handles missing file on first run. Corrupt JSON gives a readable message, not a crash.
**Self-test:** What is the difference between a shallow copy and assignment for a dict?

---

### Session 4: Git branching and GitHub
**Build:** Push your practice repo to GitHub. Create a feature branch. Make one improvement. Merge it.
Write a real README for everything you have built so far.
**Done means:** Your GitHub repo is public. README explains what each file does and how to run it.
**Self-test:** What does `git pull` do? What does `git merge` do? What is a merge conflict?

---

### Session 5: CLI tracker v2 — file-backed, indexed removal
**Build:** Upgrade your Week 1 tracker to persist data with JSON. Load on start, save on exit, reject invalid indexes.
**Done means:** Close and reopen — data survives. Bad index gives a message, not a crash.
**Self-test:** Without reading code — what happens when the save file does not exist yet?

---

### Session 6: Rebuild session — mini app from scratch
**This session has no new material.**
Close all files. Rebuild `main.py` + `validators.py` + `menu_utils.py` from memory.
It does not have to be identical. It has to work and be clean.
**Done means:** You did not copy-paste anything. It runs. You commit it as `rebuild-attempt-1`.
**Self-test:** What did you have to look up? Write it in your study log.

---

### Sessions 7–8: OOP foundations using Genshin as the domain
**Build:** Rewrite `GenshinCharacter` as a proper class, then as a dataclass.
Fields: name, level, weapon_level, constellation, talents (auto/skill/burst).
Methods: `summary()`, `is_maxed()`, `upgrade(field, amount)`.
**Done means:** `__post_init__` or `__init__` validates that no stat exceeds its cap. `is_maxed()` returns True only when all stats are at max. No global variables.
**Why Genshin:** You already understand the domain. OOP concepts land better in familiar territory.
**Self-test:** Explain encapsulation in one sentence using your `GenshinCharacter` class as the example.

---

### Session 9: OOP — CharacterRoster class + polymorphism
**Build:** `CharacterRoster` that holds a list of `GenshinCharacter` objects.
Methods: `add(character)`, `remove(name)`, `list_all()`, `list_maxed()`, `find(name)`.
Then add a subclass `TimedCharacter(GenshinCharacter)` that tracks date_added.
Run both types through the same `list_all()` loop.
**Done means:** One loop renders both types using the same interface. That is polymorphism — write that definition in your study log in your own words.

---

### Session 10: OOP checkpoint — CLI backed by your classes
**Build:** A small CLI app that uses `CharacterRoster` and `GenshinCharacter` with file persistence (JSON).
**Done means:** Add/view/remove/upgrade characters. Data persists. Classes do the work — `main.py` is just glue.
**Self-test:** What would break if you removed the class and went back to raw dicts? Write the answer.

---

## Phase 2 — SQLite Clean Patterns
### Sessions 11–15 | Weeks 3–4

**Goal:** Write SQLite CRUD you can reproduce from memory in any project.
This is a direct prerequisite for Flask. Do not rush it.

---

### Session 11: SQLite setup and first table
**Build:** `db_init.py` — creates `characters.db` and a `characters` table. Idempotent (safe to run twice).
**Done means:** Schema uses NOT NULL where appropriate. You can describe the schema without reading the file.
**Self-test:** What is a PRIMARY KEY? What does AUTOINCREMENT do? Answer from memory.

---

### Session 12: Insert and read — parameterized only
**Build:** `db_crud.py` — insert, list all, find by id. Parameterized queries only — no string formatting into SQL.
**Done means:** You inserted 3+ rows and retrieved them. You can explain why string formatting into SQL is dangerous.

---

### Session 13: Update, delete, and missing id handling
**Build:** Add update and delete helpers. Handle the case where the id does not exist gracefully.
**Done means:** Deleting id 9999 gives a clean message, not a crash. Update with bad id does the same.

---

### Session 14: Two-table schema — users and characters
**Build:** Add a `users` table. Characters belong to a user via foreign key.
**Done means:** You can insert a user, add characters for that user, and query only that user's characters.
**Self-test:** Write a SELECT query that gets all characters for user_id 1. Write it by hand before running it.

---

### Session 15: SQLite checkpoint — replace JSON tracker with SQLite
**Build:** Take your Session 5 CLI tracker. Replace the JSON file with a SQLite database.
**Done means:** DB initializes on first run. All CRUD works. You kept the DB helpers in their own file.
**Self-test:** Can you write the CREATE TABLE statement for your tracker from memory?

---

## Phase 3 — Flask Re-anchor (Build it twice)
### Sessions 16–28 | Weeks 5–8

**Goal:** Rebuild Flask auth + SQLite todo from scratch until you can do it without reference.
This is the most important phase for your job goal. Do not shortcut it.

---

### Session 16: Flask first app + structure
**Build:** Minimal Flask app with `/`, `/about`. Use a real template, not raw strings. Separate templates folder.
**Done means:** App runs. At least one Jinja template with `{% extends %}` inheritance.

---

### Session 17: Jinja templates — base + child pages
**Build:** `base.html` with nav, footer, flash message block. Two child pages that extend it.
**Done means:** No repeated HTML between pages. Flash messages render when present.

---

### Session 18: Forms and POST — GET vs POST
**Build:** A simple form that accepts text and redisplays it. Redirect-after-POST pattern. `url_for` for all redirects.
**Done means:** Blank input is rejected. Refreshing the result page does not resubmit.
**Self-test:** Why does redirect-after-POST prevent the double-submit problem?

---

### Session 19: Registration with hashed passwords
**Build:** Register route + template. Hash with `werkzeug`. Reject duplicate usernames and blank credentials.
**Done means:** You cannot register the same username twice. Passwords are never stored in plain text.
**Self-test:** Why is storing plain-text passwords unacceptable? Write the answer in your study log.

---

### Session 20: Login, logout, protected routes
**Build:** Login/logout routes. A `login_required` decorator that redirects unauthenticated users instead of crashing.
**Done means:** Bad credentials fail cleanly. Logout clears the session. Protected routes redirect instead of crash.
**Note:** Write the decorator once. Use it on every route that needs it — do not copy-paste the session check.

---

### Session 21: Todo CRUD — create and list
**Build:** Create and list todos for the current user. Blank titles rejected. User isolation — you only see your own todos.
**Done means:** Two different logged-in users cannot see each other's todos.

---

### Session 22: Todo CRUD — edit, delete, status toggle
**Build:** Edit form (prefilled). Delete. Active/inactive toggle.
**Done means:** Editing id 9999 gives a safe message. Deleting someone else's todo is blocked.

---

### Session 23: Flash messages and validation pass
**Build:** Replace all `invalid.html` redirects with flash messages on the originating page.
**Done means:** Every form error tells the user what went wrong and keeps their input visible.

---

### Session 24: Todo v1 checkpoint — README and manual test
**Write a README** that contains: how to set up, how to run, what features exist, what is not finished.
Run through a manual test checklist: auth, create/edit/delete, user isolation, bad inputs.
**Commit a tagged version:** `git tag v1.0`

---

### Session 25: REBUILD SESSION — Flask auth from scratch, no reference
Close your todo project. Open a blank folder. Rebuild register, login, logout, and one protected route from memory.
**Done means:** It works. You did not open your old code. Commit as `flask-auth-rebuild`.
**Self-test:** What did you have to look up? That list is your study target for Session 26.

---

### Session 26: Fill the gaps from Session 25
Study only the things you could not reproduce. Then rebuild just the pieces that were fuzzy.
**Done means:** You can now write a login route + session handling without reference.

---

### Session 27: REBUILD SESSION — Full todo app from scratch
Blank folder. Rebuild the entire todo app from memory. Auth + CRUD + user isolation.
Scope: registration, login, logout, create todo, list todos, delete todo. That is the MVP.
**Done means:** It works without looking at your old code. README written. Committed.

---

### Session 28: Cleanup and polish — this becomes Portfolio Project 1
Take your rebuild from Session 27 (not your original). Polish it:
- `login_required` decorator in use
- Flash messages on all errors
- Empty state messages ("No todos yet — add one above")
- Consistent styling
- README that a stranger can follow
**This is now your first portfolio project.**

---

## Phase 4 — Testing with pytest
### Sessions 29–33 | Weeks 9–10

**Goal:** Add enough testing to raise your maturity signal to employers. You do not need full coverage.

---

### Session 29: First tests — helpers and validators
**Build:** `tests/` folder. 3–5 tests on your utility functions (validators, string helpers).
**Done means:** `pytest` runs and passes. You understand what `assert` does.

---

### Session 30: Fixtures and DB helper tests
**Build:** One pytest fixture for a test database. Tests for your CRUD helpers using a temp DB.
**Done means:** Tests clean up after themselves. Real DB is never touched by tests.

---

### Session 31: Flask test client — smoke tests
**Build:** 2–3 tests using Flask's test client. At minimum: register succeeds, login fails on bad password.
**Done means:** Tests run headlessly without a real server.

---

### Session 32: Refactor for testability
Find one function in your todo app that is hard to test because it mixes concerns. Split it.
**Done means:** You can explain what made it hard to test and what you changed.

---

### Session 33: Testing checkpoint
All tests pass. README updated with test instructions (`pytest` command).
**Self-test:** What is a fixture? What is the difference between a unit test and an integration test?

---

## Phase 5 — New Portfolio Project
### Sessions 34–50 | Weeks 11–16

**Goal:** Build one project that is not a todo app and that solves a problem you understand.
This is your strongest interview artifact.

---

### Sessions 34–35: Design (2 sessions)
**Session 34 — Problem and scope:**
Write a one-page problem statement. What does this app do? Who uses it? Why does it need to exist?
Write 8–10 user stories. Mark 3 as MVP. Mark the rest as stretch.

**Session 35 — Schema, pages, and backlog:**
Draft the DB schema. List every page/route. Mark which are MVP.
Initialize the repo. Write the README skeleton now. Set up `.gitignore` and `requirements.txt`.
State explicitly in your notes what you will NOT build.

---

### Sessions 36–44: Build (9 sessions)
Work through your backlog one slice per session. Suggested order:
1. DB init + schema
2. Core list/create flow
3. Edit/delete
4. Auth (reuse your rebuild — do not start from scratch)
5. User-scoped data
6. Secondary feature (your choice from stretch goals)
7. Validation and flash message pass
8. UI consistency pass
9. Manual QA + bug fixes

---

### Sessions 45–47: Polish (3 sessions)
**Session 45:** Refactor the messiest area. Do not change behavior — improve clarity.
**Session 46:** Write tests for the highest-value helpers. Aim for 5–8 meaningful tests.
**Session 47:** Final README pass. A stranger should understand what the app does in 30 seconds.
Screenshots if useful. Tag a release: `git tag v1.0`.

---

### Sessions 48–50: Buffer
Use these for overflow, a third feature, or additional test coverage.
If you finish early, spend this time on interview prep below.

---

## Phase 6 — Portfolio and Job Preparation
### Sessions 51–60 | Weeks 17–20

---

### Session 51: GitHub profile cleanup
Pin your two best repos (Todo rebuild + new project). Write clean repo descriptions.
Every pinned repo needs: a README that explains setup in under 5 steps, a live demo or screenshots, and a clear description of the problem solved.

---

### Session 52: Project summaries — spoken
For each project, write: problem, stack, one technical challenge, one thing you would do differently.
Then say each summary out loud. Record yourself if you can stand it.
**Self-test:** Can you explain your session handling without saying "I followed a tutorial"?

---

### Session 53: Resume bullets
2–4 bullets per project. Action verb + concrete stack term + what it does.
Example pattern: "Built a Flask + SQLite habit tracker with user auth, session management, and full CRUD — deployed from scratch without a framework scaffold."
No vague filler. No "worked on" or "helped with."

---

### Session 54: Technical vocabulary practice
Write definitions from memory: session, CRUD, foreign key, decorator, fixture, parameterized query, redirect-after-POST, encapsulation, polymorphism.
Then say them out loud in a sentence, not as a definition.

---

### Session 55: Interview simulation — bug story
Write a real answer to: "Tell me about a bug you fixed."
Use only real examples from your projects. The `close_database` without parens in your todo app is a good one. The `editing` global in Genshin is another.
Structure: what the bug was → how you found it → what you changed → what you learned.

---

### Session 56: Interview simulation — design question
Write an answer to: "Walk me through how your todo app handles a user logging in."
Trace the full path: form → POST → route → DB query → session → redirect.
Say it out loud. Time yourself. Target 90 seconds.

---

### Sessions 57–60: Applications
Research role types you are targeting. Build a simple tracking spreadsheet (company, role, date, status).
Apply to 3–5 roles per week minimum. Treat application tracking as a session deliverable.

---

## Weeks 21–26 — Active job search with continued sharpening

Continue applying. Use any free sessions to:
- Add one stretch feature to your portfolio project
- Write a second set of tests
- Practice one new technical explanation per week
- Review any concept that came up in a screening or interview

---

## Study log template (unchanged — keep using this)

- What I studied today:
- What I built today:
- What broke or confused me:
- What I fixed:
- What I still had to look up:
- One thing I can now do from memory:
- Tomorrow's first task:

---

## Skill checkpoints — rate yourself 1–5 at the end of each phase

| Skill | After Phase 1 | After Phase 3 | After Phase 5 |
|---|---|---|---|
| Python syntax | | | |
| Git / GitHub | | | |
| OOP concepts | | | |
| Flask routes + templates | | | |
| SQLite CRUD | | | |
| Auth / sessions | | | |
| Testing basics | | | |
| Explaining your own code | | | |

---

## The most important thing in this plan

**Rebuild from memory.** Sessions 6, 25, 27 are the highest-value sessions in the entire plan.
Not because of what you build — because the gaps you discover are exactly what to study next.
Every time you rebuild something and get stuck, you have found a real knowledge gap.
Study notes exist to capture those gaps. The plan exists to close them.
