# Python to Employment — Full Workbook
### A Self-Study Textbook with Exercises, Questions, and Answers

---

## How to Use This Workbook

Each session is structured in four parts:

**CONCEPTS** — The textbook portion. Read this before touching code. If a concept feels vague after one read, read it again before moving on. Passive reading does not build muscle memory. Stop at each example and predict the output before reading the answer.

**CHECK YOUR UNDERSTANDING** — 5 questions per session. Answer them in writing before reading the answers. Writing forces retrieval. Retrieval builds memory. Skipping this section means skipping the most valuable part of each session.

**BUILD TASK** — The coding exercise. Requirements are listed as behavior, not implementation. That means: the spec says what it must do, not how to do it. Write the implementation yourself.

**SESSION SELF-TEST** — One or two spoken prompts. Say the answer out loud. If it sounds vague when you say it, it is vague. Add it to your study log as a gap.

---

## Daily Log Template (copy into a file called `log.md` in your repo)

```
Date:
Session number:
Session started:
Session ended:

What I studied:
What I built:
What broke:
What I fixed:
What I still had to look up:
One thing I can now do from memory that I could not before:
Tomorrow's first task:
```

---

# PHASE 1 — Python Re-anchor and Git Foundation
## Sessions 1–10 | Weeks 1–2
### Phase Goal: Write clean modular Python from memory and commit it correctly.

---

# SESSION 1
## Finish Week 1 Foundations + Git Local Setup

---

## CONCEPTS

### 1.1 How Python runs your code

When you type `python hello.py` in a terminal, the Python interpreter reads your file top to bottom, executes each line, and exits. This is different from the interactive REPL (Read-Evaluate-Print Loop) where lines are executed as you type them.

The line `if __name__ == "__main__":` exists because Python sets a special variable called `__name__` for every file it runs. When a file is run directly, `__name__` equals `"__main__"`. When a file is imported by another file, `__name__` equals the filename instead. This guard prevents code from running when a module is imported.

```python
# In file: hello.py
print(__name__)   # prints "__main__" when run directly
                  # prints "hello" when imported
```

### 1.2 Exceptions — specific catching only

An exception is a signal that something went wrong at runtime. Python raises exceptions as objects. You catch them with `try / except`.

The most important rule: **catch specific exceptions, never bare `except`.**

```python
# BAD — catches everything, including bugs you need to see
try:
    result = int(input("Number: "))
except:
    print("Something went wrong")

# GOOD — catches only what you expect
try:
    result = int(input("Number: "))
except ValueError:
    print("That was not a valid number")
```

Bare `except` catches `KeyboardInterrupt` (Ctrl+C), `SystemExit`, and actual bugs in your code. That means your program can silently swallow a logic error and continue running incorrectly.

Common exception types you will use:

| Exception | When it occurs |
|---|---|
| `ValueError` | Right type, wrong value — `int("hello")` |
| `TypeError` | Wrong type entirely — `"a" + 1` |
| `FileNotFoundError` | File path does not exist |
| `KeyError` | Dict key does not exist — `d["missing"]` |
| `IndexError` | List index out of range |
| `ZeroDivisionError` | Division by zero |

### 1.3 Safe input loops

A safe input loop retries on bad input instead of crashing. The pattern is always the same:

```python
def get_integer(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
```

`while True` loops forever until a `return` exits it. This is the correct pattern for "keep asking until valid."

### 1.4 File reading and safe handling

```python
def read_file(path: str) -> str | None:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
```

The `with` statement is a context manager. It guarantees the file is closed when the block exits, even if an exception occurs. Always use `with open(...)` — never `f = open(...)` without a paired `f.close()`.

### 1.5 Git — the three-command minimum

Git is version control. It tracks every change you commit, so you can always return to a working state.

**The three commands you use every single session:**

```bash
git status          # What files have changed?
git add .           # Stage all changes for commit
git commit -m "message"   # Save a snapshot with a label
```

**Setup (run once per project):**

```bash
git init            # Create a new repo in the current folder
```

**A `.gitignore` file** tells Git which files to never track. Create one in your project root:

```
.venv/
__pycache__/
*.pyc
.env
*.db
```

**Good commit messages** describe what changed and why, not how:

```
# BAD
git commit -m "changes"
git commit -m "fixed stuff"
git commit -m "wip"

# GOOD
git commit -m "add input validation to safe_division"
git commit -m "fix: catch ValueError instead of bare except"
git commit -m "refactor: extract get_integer into validators module"
```

Commit after every meaningful change. A session with 10 small commits is better than one large commit at the end.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What does `if __name__ == "__main__":` do, and why is it used?

**Answer:** It checks whether the file is being run directly (as the main script) or imported by another file. When run directly, `__name__` is `"__main__"` and the block executes. When imported, `__name__` is the module name and the block is skipped. This prevents code like `app.run()` or interactive input loops from firing when another file imports your module.

---

**Question 2:** What is wrong with this code?

```python
try:
    value = int(input("Enter a number: "))
    result = 100 / value
except:
    print("Invalid input")
```

**Answer:** Three problems. First, it uses bare `except` which catches everything including `KeyboardInterrupt` and actual bugs. Second, it conflates two different errors — a `ValueError` (non-numeric input) and a `ZeroDivisionError` (entering 0) should be handled separately with different messages. Third, the error message "Invalid input" is not helpful — the user does not know what was wrong. Fix:

```python
try:
    value = int(input("Enter a number: "))
except ValueError:
    print("Please enter a whole number.")
    return

try:
    result = 100 / value
except ZeroDivisionError:
    print("Cannot divide by zero.")
    return
```

---

**Question 3:** Why should you always use `with open(...)` instead of `f = open(...)`?

**Answer:** The `with` statement guarantees the file is closed when the block exits, even if an exception is raised inside the block. Without it, if your code raises an exception before `f.close()`, the file handle stays open. On some systems this causes resource leaks or prevents other processes from accessing the file.

---

**Question 4:** Write the `.gitignore` entries needed for a Python project that uses a virtual environment, has compiled Python files, and stores a local SQLite database called `app.db`.

**Answer:**
```
.venv/
__pycache__/
*.pyc
app.db
```

---

**Question 5:** What does `git status` show you, and when should you run it?

**Answer:** `git status` shows three things: untracked files (new files Git has never seen), modified files (tracked files that have changed since the last commit), and staged files (changes ready to be committed). Run it before `git add` to see what you are about to stage, and after `git add` to confirm what is staged. Running it frequently is a good habit — it keeps you aware of what state your repo is in.

---

## BUILD TASK

Build three files. Commit after each one works.

**`safe_division.py`**
- Prompt for two numbers (use a retry loop for each)
- Catch `ValueError` for non-numeric input
- Catch `ZeroDivisionError` separately — zero is a valid number to enter, it just cannot be the denominator
- Print the result formatted to 2 decimal places
- Each error gives a specific, helpful message

**`file_reader.py`**
- Accept a filename as input
- Read and print its contents
- If the file does not exist, print a helpful message and ask for another filename (retry loop)
- Use `with open(...)` only

**`retry_number_input.py`**
- A single reusable function: `get_integer(prompt: str, min_val: int, max_val: int) -> int`
- Keeps asking until the user enters a valid integer within the given range
- Demonstrates the function by asking for an age between 0 and 120

Then: `git init` your practice folder, create `.gitignore`, make at least one commit per file.

---

## SESSION SELF-TEST

Say these out loud before ending the session:

1. "The difference between `ValueError` and `TypeError` is..." 
2. "I use `with open(...)` because..."
3. "My last three commit messages were..." (check `git log`)

---

# SESSION 2
## Week 1 Checkpoint — Tracker App

---

## CONCEPTS

### 2.1 Lists — the core operations

A list is an ordered, mutable sequence. These are the operations you need to be able to write from memory:

```python
items = []                    # empty list
items.append("milk")          # add to end
items.insert(0, "eggs")       # insert at index
items.remove("milk")          # remove first occurrence (raises ValueError if missing)
items.pop(0)                  # remove and return by index (raises IndexError if empty)
popped = items.pop()          # remove and return last item
length = len(items)           # number of items
"milk" in items               # membership test — True or False
items[0]                      # index access (raises IndexError if out of range)
```

**Safe removal pattern** — always check before removing:

```python
def safe_remove(items: list, target: str) -> bool:
    if target in items:
        items.remove(target)
        return True
    print(f'"{target}" was not found in the list.')
    return False
```

### 2.2 The menu loop pattern

A menu loop is a `while True` loop that displays options, reads input, dispatches to a function, and repeats. You have already built one. The pattern is worth internalizing fully because it appears in almost every CLI app.

```python
def main() -> None:
    running = True

    def quit_app() -> None:
        nonlocal running
        running = False

    menu = {
        "1": {"label": "Add item",    "command": add_item},
        "2": {"label": "View items",  "command": view_items},
        "3": {"label": "Quit",        "command": quit_app},
    }

    while running:
        for key, entry in menu.items():
            print(f"{key}.) {entry['label']}")
        choice = input("Choose: ").strip()
        if choice in menu:
            menu[choice]["command"]()
        else:
            print("Invalid choice.")
```

`nonlocal` lets a nested function modify a variable in the enclosing (but not global) scope. Without `nonlocal running`, the assignment `running = False` would create a new local variable instead of modifying the outer one.

### 2.3 Input normalization

Always normalize user input before using it. The minimum is `.strip()` to remove leading/trailing whitespace. For list items, also consider `.lower()` for case-insensitive matching.

```python
raw = input("Add an item: ")
normalized = raw.strip().lower()
if not normalized:
    print("Item cannot be blank.")
    return
```

A blank input after `.strip()` becomes an empty string `""`. In a boolean context, `""` is falsy. So `if not normalized:` correctly catches blank input.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is the difference between `list.remove()` and `list.pop()`?

**Answer:** `remove(value)` searches for the first occurrence of a value and removes it — it raises `ValueError` if the value is not found. `pop(index)` removes and returns the item at a specific index — it raises `IndexError` if the index is out of range. `pop()` with no argument removes and returns the last item. Use `remove` when you know the value. Use `pop` when you know the position.

---

**Question 2:** Why does this not work as intended?

```python
def set_done():
    done = True

done = False
set_done()
print(done)   # prints False
```

**Answer:** `done = True` inside `set_done()` creates a new local variable called `done` that shadows the outer one. It does not modify the outer `done`. To modify the outer variable, you need either `nonlocal done` (if the function is nested inside another function that owns `done`) or `global done` (if `done` is a module-level global). Generally, passing state through return values or objects is cleaner than using `nonlocal` or `global`.

---

**Question 3:** What does `"milk" in items` do under the hood? Is it fast?

**Answer:** For a list, `in` performs a linear search — it checks each element from the beginning until it finds a match or exhausts the list. For a small list this is fine. For large lists (thousands of items), a `set` or `dict` lookup is faster because sets use hashing for O(1) average lookup. For a tracker with dozens of items, list `in` is perfectly acceptable.

---

**Question 4:** What is the output of this code?

```python
items = ["a", "b", "c", "a"]
items.remove("a")
print(items)
```

**Answer:** `['b', 'c', 'a']`. `remove()` removes only the *first* occurrence. The second `"a"` remains.

---

**Question 5:** A user types `"  Milk  "` into your tracker. After `raw.strip().lower()`, what is the value, and why does this matter?

**Answer:** The value is `"milk"`. Stripping removes the surrounding whitespace. Lowercasing normalizes case. This matters because without normalization, `"Milk"`, `"milk"`, `"  Milk  "`, and `"MILK"` would all be treated as different items. Consistent normalization prevents duplicates and makes removal by name reliable.

---

## BUILD TASK

Build `week1_tracker.py` — a single-file menu-driven list tracker.

**Required behavior:**
- Menu options: Add / View / Remove / Count / Exit
- Blank items are rejected with a message
- Removing an item that does not exist gives a message (no crash)
- Count shows the number of items currently in the list
- Invalid menu choices give a message and loop again
- The program exits cleanly on the Exit option

**Done means:** You wrote the menu loop without looking at your `menu_utils.py` from Day 5. Then compare afterward — note what you forgot.

---

## SESSION SELF-TEST

1. "The difference between `remove` and `pop` is..."
2. "I use `nonlocal` when..."
3. Run `git log --oneline`. Can you read the history and understand what changed in each commit?

---

# SESSION 3
## Dictionaries, Files, and JSON

---

## CONCEPTS

### 3.1 Dictionaries

A dictionary maps keys to values. Keys must be hashable (strings, numbers, tuples). Values can be anything.

```python
contact = {
    "name": "Alex",
    "phone": "555-1234",
    "email": "alex@example.com"
}

# Access
contact["name"]           # "Alex" — raises KeyError if missing
contact.get("fax")        # None — safe, no KeyError
contact.get("fax", "N/A") # "N/A" — default value

# Modify
contact["phone"] = "555-9999"   # update existing
contact["notes"] = "met at conf" # add new key

# Delete
del contact["notes"]
contact.pop("notes", None)  # safe delete — no KeyError if missing

# Iteration
for key, value in contact.items():
    print(f"{key}: {value}")

# Check membership
"email" in contact        # True
"fax" in contact          # False
```

### 3.2 List of dicts — the contact book pattern

Most real data is a list of records where each record is a dictionary. This is the pattern behind database rows, API responses, and CSV files.

```python
contacts: list[dict] = []

def add_contact(name: str, phone: str, email: str) -> None:
    contacts.append({
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip()
    })

def find_contact(name: str) -> dict | None:
    for contact in contacts:
        if contact["name"].lower() == name.strip().lower():
            return contact
    return None
```

### 3.3 JSON — saving and loading structured data

JSON (JavaScript Object Notation) is a text format for storing structured data. Python's `json` module converts between Python dicts/lists and JSON strings.

```python
import json

# Saving — Python object → JSON file
def save_data(data: list, path: str) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Loading — JSON file → Python object
def load_data(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []           # first run — no file yet
    except json.JSONDecodeError:
        print("Warning: save file is corrupted. Starting fresh.")
        return []
```

Two exceptions to handle:
- `FileNotFoundError` — normal on first run, return an empty list
- `json.JSONDecodeError` — file exists but is not valid JSON (truncated save, manual editing mistake)

**`json.dump` vs `json.dumps`:** `dump` writes to a file object. `dumps` returns a string. Same for `load` vs `loads`.

### 3.4 The save/load contract

Every persistent app has a contract: data written by `save` must be readable by `load`. Keep them in the same file and test them together.

```python
SAVE_FILE = "contacts.json"

def save() -> None:
    save_data(contacts, SAVE_FILE)

def load() -> None:
    global contacts
    contacts = load_data(SAVE_FILE)
```

Call `load()` once at startup. Call `save()` after every mutation. This is the simplest correct pattern.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is the difference between `dict["key"]` and `dict.get("key")`?

**Answer:** `dict["key"]` raises `KeyError` if the key does not exist. `dict.get("key")` returns `None` if the key does not exist (or a provided default: `dict.get("key", "default")`). Use bracket access when the key must exist and its absence is a bug. Use `.get()` when the key may legitimately be absent.

---

**Question 2:** What are the two exceptions you should handle when loading a JSON file, and what does each mean?

**Answer:** `FileNotFoundError` means the file does not exist yet — this is normal on first run and should be handled by returning an empty collection. `json.JSONDecodeError` means the file exists but cannot be parsed as valid JSON — this happens when a save was interrupted, the file was manually edited incorrectly, or the file is the wrong type. Both should return a safe empty state rather than crashing.

---

**Question 3:** What is the difference between `json.dump` and `json.dumps`?

**Answer:** `json.dump(data, file_object)` writes JSON directly to a file. `json.dumps(data)` returns a JSON-formatted string. The `s` stands for "string." Use `dump` when writing to a file, `dumps` when you need the JSON as a string in memory (for logging, APIs, etc.).

---

**Question 4:** Given this list of dicts, write a function that returns the contact with the matching name, case-insensitively, or `None` if not found.

```python
contacts = [
    {"name": "Alice", "phone": "555-1111"},
    {"name": "Bob",   "phone": "555-2222"},
]
```

**Answer:**
```python
def find_by_name(name: str) -> dict | None:
    target = name.strip().lower()
    for contact in contacts:
        if contact["name"].lower() == target:
            return contact
    return None
```

---

**Question 5:** Why is `indent=2` passed to `json.dump`, and what happens without it?

**Answer:** `indent=2` formats the JSON with 2-space indentation, making it human-readable. Without it, `json.dump` produces a single-line compact string. Both are valid JSON and load identically. The indented version is much easier to read and debug in a text editor, which is why it is used during development.

---

## BUILD TASK

Build `contact_book.py`:
- Add contacts (name, phone, email — name is required, others optional)
- List all contacts
- Find a contact by name (case-insensitive)
- Remove a contact by name
- Save to `contacts.json` on every change
- Load from `contacts.json` on startup (handle missing file and corrupt file)
- Reject blank names

**Done means:** Close the program, reopen it — all contacts are still there.

---

## SESSION SELF-TEST

1. "The difference between `dict['key']` and `dict.get('key')` is..."
2. "When I load a JSON file, I handle two exceptions because..."

---

# SESSION 4
## Git Branching and GitHub

---

## CONCEPTS

### 4.1 Why branching matters

A branch is an independent line of development. `main` is your stable branch — it always contains working code. Feature branches let you experiment without breaking `main`.

The mental model: think of `main` as the published version of your code. You never edit the published version directly. You write a draft (feature branch), review it, then publish (merge).

### 4.2 Essential branch commands

```bash
# Create and switch to a new branch
git checkout -b feature/add-email-validation

# See all branches (* = current)
git branch

# Switch between branches
git checkout main
git checkout feature/add-email-validation

# Merge a branch into current branch
git checkout main
git merge feature/add-email-validation

# Delete a branch after merging
git branch -d feature/add-email-validation
```

### 4.3 What a merge conflict looks like

A merge conflict happens when two branches changed the same line differently. Git cannot decide which version is correct, so it marks both:

```python
<<<<<<< HEAD
def greet(name: str) -> str:
    return f"Hello, {name}!"
=======
def greet(name: str) -> str:
    return f"Hi there, {name}!"
>>>>>>> feature/update-greeting
```

To resolve: delete the markers, keep the version you want (or combine them), save, then `git add` and `git commit`.

### 4.4 GitHub — remote repositories

GitHub is a hosting service for Git repositories. Your local repo and the GitHub repo are separate — you sync them with `push` and `pull`.

```bash
# Link your local repo to GitHub (run once, after creating repo on github.com)
git remote add origin https://github.com/username/repo-name.git

# Push local commits to GitHub
git push origin main

# Pull changes from GitHub to local
git pull origin main

# Push a new branch to GitHub
git push origin feature/add-email-validation
```

**First-time setup:**
1. Create the repo on github.com (click New Repository)
2. Copy the HTTPS URL
3. Run `git remote add origin <url>` in your local project
4. Run `git push -u origin main` (the `-u` sets the default upstream)

### 4.5 A README worth writing

A README is the first thing anyone (including future you) reads. It must answer:
1. What does this project do?
2. How do I set it up?
3. How do I run it?

Minimum template:
```markdown
# Project Name

Brief description in one sentence.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Features
- Feature 1
- Feature 2
```

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is the purpose of a feature branch?

**Answer:** A feature branch isolates new work from the stable `main` branch. You develop on the branch, and only merge it into `main` when it is working. This means `main` always stays in a runnable state. If something goes wrong on the branch, you can discard it without affecting `main`.

---

**Question 2:** What sequence of commands pushes a new feature branch to GitHub?

**Answer:**
```bash
git checkout -b feature/my-feature   # create branch
# ... make changes, git add, git commit ...
git push origin feature/my-feature   # push to GitHub
```

---

**Question 3:** What does `git pull` do?

**Answer:** `git pull` fetches changes from the remote (GitHub) and merges them into your current local branch. It is equivalent to `git fetch` followed by `git merge`. Use it when you have been away from a project and want to bring your local copy up to date with whatever is on GitHub.

---

**Question 4:** You are on `main` and run `git merge feature/login`. Git reports a conflict in `app.py`. What are the exact steps to resolve it?

**Answer:** 
1. Open `app.py` in your editor
2. Find the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Delete the markers and keep the correct code (yours, theirs, or a combination)
4. Save the file
5. `git add app.py`
6. `git commit -m "resolve merge conflict in app.py"`

---

**Question 5:** What is the difference between `git add .` and `git add filename.py`?

**Answer:** `git add .` stages all changed files in the current directory (and subdirectories). `git add filename.py` stages only that specific file. Use specific file staging when you have made changes you are not ready to commit alongside the changes you are. Use `git add .` when all changes belong in the same commit.

---

## BUILD TASK

1. Push your practice repo to GitHub (create the repo on github.com first)
2. Create a branch called `feature/improve-contact-book`
3. Add one improvement to `contact_book.py` (a search feature, a sort, an edit function)
4. Commit the improvement on the branch
5. Merge the branch back to `main`
6. Write a real README for your project (setup + run + features)
7. Push the updated `main` to GitHub

**Done means:** Your GitHub repo is public and a stranger can read the README and know what to run.

---

## SESSION SELF-TEST

1. "The reason I use feature branches instead of committing directly to `main` is..."
2. Go to your GitHub repo in a browser. Click on a commit. Can you see the diff? Do the messages explain the changes?

---

# SESSION 5
## CLI Tracker v2 — File-Backed Storage

---

## CONCEPTS

### 5.1 Persistent state — the load/mutate/save cycle

Any application that needs to remember data across runs follows the same three-step cycle:

1. **Load** on startup — read from disk into memory
2. **Mutate** during the session — change the in-memory data
3. **Save** on change (or on exit) — write from memory to disk

The decision between "save on every change" and "save on exit" depends on your risk tolerance. Save on every change is safer — a crash does not lose the last session. Save on exit is faster for large datasets. For small CLI apps, save on every change.

### 5.2 Indexed removal

When displaying a numbered list, the user should be able to remove by number rather than by typing the full name. This is more reliable and faster.

```python
def view_items(items: list) -> None:
    if not items:
        print("No items yet.")
        return
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")

def remove_by_index(items: list, raw_index: str) -> bool:
    try:
        index = int(raw_index) - 1    # convert to 0-based
        if index < 0 or index >= len(items):
            print(f"No item at position {raw_index}.")
            return False
        removed = items.pop(index)
        print(f'Removed: "{removed}"')
        return True
    except ValueError:
        print("Please enter a number.")
        return False
```

Note: `enumerate(items, start=1)` numbers items from 1 in the display. The user sees 1-based numbers. You subtract 1 when converting back to a list index. This is the correct pattern — never show users 0-based indexes.

### 5.3 Module structure — separating concerns

A well-structured CLI app has at least three layers:
- **Storage** — load and save (knows about files, knows nothing about menus)
- **Logic** — add, remove, find (knows about data, knows nothing about display)  
- **Interface** — menus, display, input (knows about the user, delegates work to logic)

For a small app these can be in one file with clear sections. For a larger app they become separate modules. The principle is the same: each function should have one job.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** Why is saving on every change safer than saving only on exit?

**Answer:** If the program crashes, raises an uncaught exception, or the system loses power before the exit save runs, all changes from that session are lost. Saving on every mutation means you lose at most the last operation. The tradeoff is slightly slower performance due to more file writes, which is negligible for small datasets.

---

**Question 2:** A user enters "0" as an index for a 5-item list. What should happen?

**Answer:** The index 0, converted to 0-based, would be -1. But even before that — checking `if index < 0` catches this case. The user should see a message like "No item at position 0" because valid positions in a 1-based display are 1 through 5. Negative list indexes are valid Python (they index from the end), so you must explicitly reject them.

---

**Question 3:** What does `enumerate(items, start=1)` return?

**Answer:** It returns an iterator of `(index, value)` tuples where the index starts at 1 instead of the default 0. For `items = ["milk", "eggs"]`, it yields `(1, "milk")` then `(2, "eggs")`. Used in a `for i, item in enumerate(items, start=1):` loop, `i` is the display number and `item` is the value.

---

**Question 4:** Why should you never show users 0-based indexes in a display?

**Answer:** Users count from 1. Showing "item 0" violates natural expectations and leads to off-by-one errors when the user tries to act on it. Always display 1-based numbers, convert to 0-based internally when accessing the list.

---

**Question 5:** What is the single responsibility principle, in plain English?

**Answer:** Each function (or module) should do one thing and do it well. A function that reads a file, validates the data, and prints a menu is doing three things — split it into three functions. This makes each function easier to test, easier to understand, and easier to change without breaking something else.

---

## BUILD TASK

Upgrade your Session 2 tracker (`week1_tracker.py`) to create `tracker_v2.py`:
- Items persist to `tracker.json`
- Load on start (safe — handle missing and corrupt file)
- Save after every add and remove
- Remove by index number (displayed 1-based)
- Entering an invalid index gives a message, not a crash
- Entering a non-numeric index gives a message, not a crash

**Done means:** Run the program. Add 3 items. Exit. Reopen. Items are still there. Enter "999" as a remove index — it gives a message. Enter "abc" as a remove index — it gives a message.

---

## SESSION SELF-TEST

1. "The load/mutate/save cycle means..."
2. "I show 1-based indexes in the display because..."

---

# SESSION 6
## Rebuild Session — Mini App From Scratch

---

## CONCEPTS

This session has no new concepts. Its purpose is retrieval practice — the most powerful learning technique for programming.

### Why rebuilding matters more than re-reading

Reading your own code feels like understanding. It is not. When you read code you wrote, your brain fills in the gaps automatically — you see what you intended, not what is actually there.

Rebuilding from memory bypasses this. When you have to produce the code without seeing it, every genuine gap becomes visible immediately. You cannot fake your way through a blank editor.

The gaps you discover in this session are more valuable than any tutorial. They tell you exactly what to study next.

### How to do this session correctly

1. Close all your previous code files
2. Close your notes
3. Open a new folder
4. Build `main.py`, `validators.py`, and `menu_utils.py` from memory
5. When you get stuck, write down exactly what you are stuck on
6. Keep going with a placeholder (a function that just prints "TODO") and come back

Do not open your old code until the rebuild is committed.

---

## CHECK YOUR UNDERSTANDING

Answer these before starting the rebuild. No notes.

**Question 1:** Write the signature and body of `safe_float(text: str) -> float | None` from memory.

**Model answer:**
```python
def safe_float(text: str) -> float | None:
    try:
        return float(text.strip())
    except ValueError:
        return None
```

---

**Question 2:** Write the `show_menu` function from memory.

**Model answer:**
```python
def show_menu(menu: dict) -> None:
    print()
    for key, entry in menu.items():
        print(f"{key}.) {entry['label']}")
    print()
```

---

**Question 3:** Write the `handle_input` function from memory.

**Model answer:**
```python
def handle_input(user_input: str, menu: dict) -> None:
    if not user_input.strip():
        print("Input cannot be blank.")
        return
    if user_input in menu:
        menu[user_input]["command"]()
    else:
        print("Invalid option, try again.")
```

---

**Question 4:** Write the `clean_text` function from memory.

**Model answer:**
```python
def clean_text(text: str) -> str:
    return " ".join(text.strip().split())
```

---

**Question 5:** Write the `is_nonempty` function from memory.

**Model answer:**
```python
def is_nonempty(text: str) -> bool:
    return bool(text.strip())
```

---

## BUILD TASK

Rebuild the following from memory. No looking at old code.

- `main.py` — menu loop with at least 3 options plus exit
- `validators.py` — `safe_float`, `is_nonempty`, `get_two_float`, `format_number`
- `menu_utils.py` — `show_menu`, `handle_input`, `MenuEntry` TypedDict, `MenuDict` type alias
- `string_utils.py` — `clean_text`, `word_count`

Commit the rebuild as `rebuild-attempt-1`.

Then open your original code. Write in your study log:
- What you got right
- What you forgot
- What you wrote differently (and whether your version is actually better)

---

## SESSION SELF-TEST

Read your study log entry for this session. The things you forgot are your study targets. Mark them. You will see them again.

---

# SESSION 7
## OOP Foundations — GenshinCharacter Class

---

## CONCEPTS

### 7.1 Why classes exist

A class bundles data and the functions that operate on that data into one unit. Without classes, related data lives in loose dictionaries and functions that accept those dictionaries scatter across files with no enforced contract.

```python
# Without a class — fragile, no contract enforced
character = {"name": "Diluc", "level": 1, "weapon_level": 1}
character["level"] = 200  # accidentally invalid, nothing catches it

# With a class — data and rules live together
class GenshinCharacter:
    MAX_LEVEL = 90

    def __init__(self, name: str, level: int = 1):
        if not name.strip():
            raise ValueError("Character name cannot be blank")
        self.name = name.strip()
        self.level = min(level, self.MAX_LEVEL)
```

### 7.2 `__init__` — the constructor

`__init__` runs when you create an instance. `self` refers to the instance being created.

```python
class GenshinCharacter:
    MAX_LEVEL = 90
    MAX_WEAPON = 90
    MAX_TALENT = 10
    MAX_CONSTELLATION = 6

    def __init__(
        self,
        name: str,
        level: int = 1,
        weapon_level: int = 1,
        constellation: int = 0,
        talent_auto: int = 1,
        talent_skill: int = 1,
        talent_burst: int = 1,
    ) -> None:
        if not name.strip():
            raise ValueError("Name cannot be blank")
        self.name = name.strip()
        self.level = self._clamp(level, 1, self.MAX_LEVEL)
        self.weapon_level = self._clamp(weapon_level, 1, self.MAX_WEAPON)
        self.constellation = self._clamp(constellation, 0, self.MAX_CONSTELLATION)
        self.talent_auto = self._clamp(talent_auto, 1, self.MAX_TALENT)
        self.talent_skill = self._clamp(talent_skill, 1, self.MAX_TALENT)
        self.talent_burst = self._clamp(talent_burst, 1, self.MAX_TALENT)

    def _clamp(self, value: int, min_val: int, max_val: int) -> int:
        return max(min_val, min(max_val, value))
```

### 7.3 Instance methods

Methods are functions defined inside a class. They always take `self` as the first argument.

```python
    def summary(self) -> str:
        return (
            f"{self.name} | Lv {self.level} | "
            f"Weapon Lv {self.weapon_level} | "
            f"C{self.constellation} | "
            f"Talents: {self.talent_auto}/{self.talent_skill}/{self.talent_burst}"
        )

    def is_maxed(self) -> bool:
        return (
            self.level == self.MAX_LEVEL
            and self.weapon_level == self.MAX_WEAPON
            and self.talent_auto == self.MAX_TALENT
            and self.talent_skill == self.MAX_TALENT
            and self.talent_burst == self.MAX_TALENT
        )
```

### 7.4 Encapsulation

Encapsulation means keeping the internal state of an object private and providing controlled access through methods. The underscore prefix `_method` is Python's convention for "internal use, do not call from outside the class."

```python
    def upgrade(self, field: str, amount: int) -> None:
        caps = {
            "level": self.MAX_LEVEL,
            "weapon_level": self.MAX_WEAPON,
            "talent_auto": self.MAX_TALENT,
            "talent_skill": self.MAX_TALENT,
            "talent_burst": self.MAX_TALENT,
        }
        if field not in caps:
            raise ValueError(f"Unknown field: {field}")
        current = getattr(self, field)
        setattr(self, field, self._clamp(current + amount, 1, caps[field]))
```

The `upgrade` method is the controlled channel for changing stats. Calling `character.level = 999` from outside the class bypasses the cap — which is why real projects use `@property` with setters. For now, using methods for mutations is the correct approach.

### 7.5 Class variables vs instance variables

```python
class GenshinCharacter:
    MAX_LEVEL = 90    # class variable — shared by all instances

    def __init__(self):
        self.name = ""   # instance variable — unique to each instance
```

Class variables are accessed as `GenshinCharacter.MAX_LEVEL` or `self.MAX_LEVEL`. Instance variables are only on the instance.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is `self`, and why does every method take it as the first argument?

**Answer:** `self` is a reference to the specific instance the method is being called on. When you write `character.summary()`, Python translates this to `GenshinCharacter.summary(character)` — it passes the instance as the first argument automatically. `self` is just a convention; you could name it anything, but you should not.

---

**Question 2:** What is the difference between a class variable and an instance variable?

**Answer:** A class variable is defined in the class body outside `__init__` and is shared by all instances. Changing it on the class changes it for all instances. An instance variable is defined inside `__init__` with `self.name` and belongs only to that specific instance. Each instance has its own copy.

---

**Question 3:** Why is the `_clamp` helper method named with a leading underscore?

**Answer:** The underscore prefix is Python's convention for "private" — it signals to other programmers that this method is an internal implementation detail and should not be called from outside the class. Python does not enforce this, but it is a strong convention. The clamp logic is not part of the public interface of the character — it is just a utility used internally.

---

**Question 4:** What does `getattr(self, field)` do, and when is it useful?

**Answer:** `getattr(object, name)` is equivalent to `object.name` but where `name` is a string variable. `getattr(self, "level")` is the same as `self.level`. It is useful when you need to access attributes dynamically — when you do not know at write time which attribute you need. `setattr(object, name, value)` is the equivalent for setting. Used in the `upgrade` method to update any stat by name.

---

**Question 5:** What happens if you call `GenshinCharacter("")`?

**Answer:** The `__init__` method checks `if not name.strip():` and raises `ValueError("Name cannot be blank")`. The object is never created. The caller should catch this `ValueError` and display an appropriate message to the user.

---

## BUILD TASK

Build `genshin_character.py` with a full `GenshinCharacter` class:
- `__init__` with all fields, clamped to their maximums
- `summary()` → formatted string
- `is_maxed()` → True only when all stats are at their maximum
- `upgrade(field, amount)` → increments a stat by amount, respects cap
- Blank name raises `ValueError`

Test it in a `__main__` block:
```python
if __name__ == "__main__":
    c = GenshinCharacter("Diluc", level=80, weapon_level=80)
    print(c.summary())
    c.upgrade("level", 15)
    print(c.summary())
    print("Maxed:", c.is_maxed())
```

Commit when the output looks correct.

---

## SESSION SELF-TEST

1. "Encapsulation means..."
2. "I use methods for mutations instead of direct attribute access because..."

---

# SESSION 8
## OOP — Dataclasses

---

## CONCEPTS

### 8.1 What dataclasses do

A `dataclass` is a class with reduced boilerplate. Python generates `__init__`, `__repr__`, and `__eq__` for you based on field declarations.

```python
from dataclasses import dataclass, field

@dataclass
class GenshinCharacter:
    name: str
    level: int = 1
    weapon_level: int = 1
    constellation: int = 0
    talent_auto: int = 1
    talent_skill: int = 1
    talent_burst: int = 1

    MAX_LEVEL: int = field(default=90, repr=False, compare=False)
```

This generates a complete `__init__` accepting all fields, a `__repr__` that prints the field values, and `__eq__` that compares by field values.

### 8.2 `__post_init__` for validation

When you need to validate or transform data after the generated `__init__` runs, use `__post_init__`:

```python
from dataclasses import dataclass

@dataclass
class GenshinCharacter:
    name: str
    level: int = 1

    MAX_LEVEL: int = field(default=90, init=False, repr=False)

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be blank")
        self.name = self.name.strip()
        self.level = max(1, min(self.MAX_LEVEL, self.level))
```

`init=False` means the field is not included in the generated `__init__` — it is set only by the class.

### 8.3 When to use a dataclass vs a regular class

Use a dataclass when:
- The class is primarily a data container
- You want auto-generated `__init__`, `__repr__`, `__eq__`
- The fields are straightforward

Use a regular class when:
- `__init__` is complex
- You need `__slots__` for memory efficiency
- You are subclassing something that does not play well with dataclasses
- The generated methods would be wrong

For `GenshinCharacter`, a dataclass is appropriate. The `__post_init__` handles the validation that the generated `__init__` cannot do alone.

### 8.4 Comparing the two versions

```python
# Regular class (Session 7)
class GenshinCharacter:
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
    
    def __repr__(self):
        return f"GenshinCharacter(name={self.name!r}, level={self.level})"
    
    def __eq__(self, other):
        return self.name == other.name and self.level == other.level

# Dataclass (Session 8) — equivalent, much shorter
from dataclasses import dataclass

@dataclass
class GenshinCharacter:
    name: str
    level: int = 1
```

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What three methods does `@dataclass` auto-generate?

**Answer:** `__init__` (the constructor, accepting all declared fields), `__repr__` (a string representation showing all field names and values), and `__eq__` (equality comparison based on all field values). You can customize which are generated with parameters to `@dataclass(repr=False, eq=False, etc.)`.

---

**Question 2:** When does `__post_init__` run?

**Answer:** `__post_init__` runs automatically at the end of the generated `__init__`. Use it for any validation or transformation that cannot be done in the field declarations themselves — like checking that a string is non-empty, clamping a number to a range, or computing a derived field.

---

**Question 3:** What does `field(default=90, init=False, repr=False)` do?

**Answer:** `field()` gives fine-grained control over a dataclass field. `default=90` sets the default value. `init=False` means this field is NOT included in the generated `__init__` — it cannot be passed as a constructor argument. `repr=False` means it is excluded from the auto-generated `__repr__`. This is used for constants that should not be settable from outside.

---

**Question 4:** Would a regular class or a dataclass be better for a `DatabaseConnection` class that takes a path, opens a connection in `__init__`, and has methods for CRUD operations?

**Answer:** A regular class. A `DatabaseConnection` is not primarily a data container — it manages a resource (the connection) and has complex behavior. The auto-generated `__repr__` and `__eq__` would not make sense for it (two connections to the same file are not equal in the way dataclass equality works). The complexity of `__init__` (opening the connection, error handling) also belongs in hand-written code.

---

**Question 5:** How do you tell a dataclass field to use a list as its default value?

**Answer:** You cannot use a mutable object (like `[]`) directly as a default in a dataclass — Python would share the same list object across all instances. Instead, use `field(default_factory=list)`:

```python
from dataclasses import dataclass, field

@dataclass
class CharacterRoster:
    characters: list = field(default_factory=list)
```

This calls `list()` (creating a new empty list) for each new instance.

---

## BUILD TASK

Convert your `GenshinCharacter` from Session 7 to a dataclass:
- Use `@dataclass`
- Use `__post_init__` for validation and clamping
- Keep `summary()`, `is_maxed()`, and `upgrade()` as regular methods
- Use `field(default_factory=...)` if you add any list or dict fields
- Write a brief comment noting what dataclass gave you for free vs what you still write manually

Commit and note in your study log: what did you gain from the dataclass? What did you lose (if anything)?

---

## SESSION SELF-TEST

1. "The three things `@dataclass` generates automatically are..."
2. "I use `__post_init__` instead of putting validation in `__init__` because..."

---

# SESSION 9
## OOP — CharacterRoster and Polymorphism

---

## CONCEPTS

### 9.1 Composition — objects that contain objects

A `CharacterRoster` holds a list of `GenshinCharacter` objects. This is composition — one class uses another class as a component.

```python
from dataclasses import dataclass, field
from genshin_character import GenshinCharacter

@dataclass
class CharacterRoster:
    characters: list[GenshinCharacter] = field(default_factory=list)

    def add(self, character: GenshinCharacter) -> None:
        self.characters.append(character)

    def remove(self, name: str) -> bool:
        for i, c in enumerate(self.characters):
            if c.name.lower() == name.strip().lower():
                self.characters.pop(i)
                return True
        return False

    def find(self, name: str) -> GenshinCharacter | None:
        for c in self.characters:
            if c.name.lower() == name.strip().lower():
                return c
        return None

    def list_all(self) -> None:
        if not self.characters:
            print("No characters yet.")
            return
        for c in self.characters:
            print(c.summary())

    def list_maxed(self) -> None:
        maxed = [c for c in self.characters if c.is_maxed()]
        if not maxed:
            print("No maxed characters.")
            return
        for c in maxed:
            print(c.summary())
```

### 9.2 Inheritance

Inheritance creates an "is-a" relationship. A `TimedCharacter` IS a `GenshinCharacter` with an additional `date_added` field.

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class TimedCharacter(GenshinCharacter):
    date_added: date = field(default_factory=date.today)

    def summary(self) -> str:
        base = super().summary()
        return f"{base} | Added: {self.date_added}"
```

`super().summary()` calls the parent class's `summary()` method. This lets you extend behavior without rewriting it.

### 9.3 Polymorphism

Polymorphism means one interface works on multiple types. Because `TimedCharacter` inherits from `GenshinCharacter`, any code that works with `GenshinCharacter` automatically works with `TimedCharacter` too.

```python
roster = CharacterRoster()
roster.add(GenshinCharacter("Diluc", level=90))
roster.add(TimedCharacter("Hu Tao", level=80))

# This loop works on both types without special-casing
for character in roster.characters:
    print(character.summary())   # calls the right summary() for each type
```

Python uses duck typing — if the object has a `summary()` method, you can call it. You do not need `isinstance` checks. This is polymorphism in practice.

### 9.4 When to use inheritance vs composition

Use **inheritance** when: the child genuinely IS a more specific version of the parent. `TimedCharacter` IS a `GenshinCharacter` with a date — this is appropriate inheritance.

Use **composition** when: you want the behavior but there is no IS-A relationship. `CharacterRoster` HAS characters — it does not IS-A character. Composition is more flexible and less likely to cause problems as requirements change.

The rule of thumb: if you find yourself saying "X IS a Y", inheritance may apply. If you find yourself saying "X HAS a Y" or "X USES a Y", use composition.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is the difference between inheritance and composition?

**Answer:** Inheritance is an IS-A relationship — a subclass extends a parent class and gets all its methods and attributes. Composition is a HAS-A relationship — a class contains an instance of another class as an attribute. Inheritance creates tight coupling between classes; composition is more flexible and easier to change.

---

**Question 2:** What does `super().summary()` do?

**Answer:** `super()` returns a proxy to the parent class. `super().summary()` calls the `summary()` method of the parent class (`GenshinCharacter`) rather than the current class's version. This allows the subclass to extend the parent's behavior by calling it and then adding to it.

---

**Question 3:** What is duck typing?

**Answer:** Duck typing is the Python approach to polymorphism: if an object has the method or attribute you need, you can use it, regardless of its type. The name comes from "if it walks like a duck and quacks like a duck, it's a duck." Python does not require explicit interface declarations — any object with a `summary()` method can be passed to code that calls `summary()`.

---

**Question 4:** Why does this code work?

```python
characters = [GenshinCharacter("Diluc"), TimedCharacter("Hu Tao")]
for c in characters:
    print(c.summary())
```

**Answer:** Both `GenshinCharacter` and `TimedCharacter` have a `summary()` method. Python looks up the method on each object at runtime (dynamic dispatch), so it calls `GenshinCharacter.summary()` for the first and `TimedCharacter.summary()` for the second. This is polymorphism — the same line of code (`c.summary()`) produces different behavior depending on the type of `c`.

---

**Question 5:** When you call `TimedCharacter("Hu Tao", level=80)`, what happens in `__init__`?

**Answer:** Python calls the dataclass-generated `__init__` of `TimedCharacter`, which includes all fields from the parent (`GenshinCharacter`) plus the new `date_added` field. The parent's `__post_init__` also runs if it is defined, handling validation. The subclass inherits the parent's `__post_init__` unless it overrides it.

---

## BUILD TASK

1. Build `character_roster.py` with the `CharacterRoster` class (add, remove, find, list_all, list_maxed)
2. Build `timed_character.py` with `TimedCharacter(GenshinCharacter)` that adds `date_added` and overrides `summary()`
3. Build a `__main__` demo that:
   - Creates a roster
   - Adds 2 regular characters and 1 timed character
   - Calls `list_all()` — confirm both types render
   - Upgrades one character to max and calls `list_maxed()`

Write in your study log: What is the difference between inheritance and composition in your own words, using your code as the example.

---

## SESSION SELF-TEST

1. "Polymorphism means... and I used it when..."
2. "I chose composition for CharacterRoster instead of inheritance because..."

---

# SESSION 10
## OOP Checkpoint — CLI Backed by Classes

---

## CONCEPTS

### 10.1 JSON and custom objects

`json.dump` and `json.load` work with Python's basic types: dicts, lists, strings, numbers, booleans, None. They do not know about your custom classes. You need to convert your objects to dicts before saving and reconstruct them from dicts when loading.

```python
# Convert object → dict
def character_to_dict(c: GenshinCharacter) -> dict:
    return {
        "name": c.name,
        "level": c.level,
        "weapon_level": c.weapon_level,
        "constellation": c.constellation,
        "talent_auto": c.talent_auto,
        "talent_skill": c.talent_skill,
        "talent_burst": c.talent_burst,
    }

# Convert dict → object
def character_from_dict(d: dict) -> GenshinCharacter:
    return GenshinCharacter(
        name=d["name"],
        level=d["level"],
        weapon_level=d["weapon_level"],
        constellation=d["constellation"],
        talent_auto=d["talent_auto"],
        talent_skill=d["talent_skill"],
        talent_burst=d["talent_burst"],
    )
```

### 10.2 Keeping `main.py` as glue

In a well-structured app, `main.py` does almost nothing:
- Creates the objects
- Calls load
- Runs the menu loop
- Calls save

All logic belongs in the classes or utility modules. If your `main.py` has more than ~50 lines, push logic down into the classes.

```python
# main.py — just glue
from character_roster import CharacterRoster
from persistence import load_roster, save_roster

def main():
    roster = load_roster()

    menu = {
        "1": {"label": "Add character", "command": lambda: add_character(roster)},
        "2": {"label": "List all",      "command": roster.list_all},
        "3": {"label": "List maxed",    "command": roster.list_maxed},
        "4": {"label": "Upgrade",       "command": lambda: upgrade_character(roster)},
        "5": {"label": "Exit",          "command": lambda: exit_app(roster)},
    }
    # ...
```

---

## CHECK YOUR UNDERSTANDING

**Question 1:** Why can't you pass a `GenshinCharacter` object directly to `json.dump`?

**Answer:** `json.dump` only handles Python built-in types: dict, list, str, int, float, bool, None. A custom class instance is not one of these. You must serialize it to a dict (or other basic type) first, and deserialize it back when loading.

---

**Question 2:** What is the risk of saving and loading the character name as-is without any validation in `character_from_dict`?

**Answer:** If the JSON file was manually edited or corrupted, the name field could be missing, empty, or the wrong type. `GenshinCharacter(name=d["name"])` would raise a `KeyError` if `"name"` is missing, or a `ValueError` from `__post_init__` if it is blank. `character_from_dict` should either handle these cases or let the exception propagate so the caller can handle corrupt data.

---

**Question 3:** A classmate argues you should store characters as dicts throughout the whole app instead of using a class, to avoid the serialization step. What is the argument against this?

**Answer:** With dicts you lose: validation (nothing prevents `character["level"] = 999`), methods (`character.is_maxed()` becomes a standalone function that must be passed the dict), encapsulation (any code can modify any field), and IDE support (no autocomplete on dict keys). The serialization step is a small, isolated cost. The benefits of the class pay dividends throughout the entire codebase.

---

**Question 4:** What does a lambda in a menu dict do?

**Answer:** A lambda is an anonymous inline function. In a menu dict, `"command": lambda: add_character(roster)` creates a zero-argument function that calls `add_character(roster)` when invoked. It is needed because the menu dict stores callables that take no arguments, but `add_character` needs `roster` as a parameter. The lambda captures `roster` from the enclosing scope.

---

**Question 5:** Name three signs that your `main.py` has too much logic in it.

**Answer:** Any of: (1) It contains SQL queries or file I/O directly instead of calling helpers. (2) It contains validation logic like checking if a string is blank. (3) It has branches (if/else) that belong to business logic rather than menu dispatch. (4) It is longer than ~60–80 lines. (5) You cannot understand what a function in it does without reading the whole file.

---

## BUILD TASK

Build a small CLI app that uses `CharacterRoster` and `GenshinCharacter`:
- Add a character (with validation — blank name, invalid stats give messages)
- List all characters
- List maxed characters
- Upgrade a character by name (choose which stat, how much)
- Save to `characters.json` on every change
- Load on startup

**Structure requirements:**
- `genshin_character.py` — the class (unchanged from Session 7/8)
- `character_roster.py` — the roster class
- `persistence.py` — `save_roster()` and `load_roster()` only
- `main.py` — menu loop and input handling only, ~50 lines max

**Done means:** Add 3 characters. Exit. Reopen. Characters load. Upgrade one. Exit. Reopen. Upgrade persisted.

---

## SESSION SELF-TEST

1. "The reason I can't pass a class instance directly to `json.dump` is..."
2. "My `main.py` is the right size if..."

---

# PHASE 1 SKILL CHECKPOINT

Before starting Phase 2, rate yourself honestly on each skill (1 = cannot do without heavy reference, 5 = can do from memory):

| Skill | Rating | What I still need to practice |
|---|---|---|
| Writing a safe input loop | | |
| Catching specific exceptions | | |
| Reading and writing JSON files | | |
| Writing a class with `__init__` and methods | | |
| Writing a dataclass with `__post_init__` | | |
| Inheritance and `super()` | | |
| Git: init, add, commit, push | | |
| Git: create branch, merge, delete branch | | |
| Explaining encapsulation out loud | | |
| Explaining polymorphism out loud | | |

If any rating is below 3, add a review task at the start of the next session before moving forward.
