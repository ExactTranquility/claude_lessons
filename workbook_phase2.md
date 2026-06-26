# Python to Employment — Workbook
# PHASE 2 — SQLite Clean Patterns
## Sessions 11–15 | Weeks 3–4

### Phase Goal
Write SQLite CRUD that you can reproduce from memory in any project. Every Flask app you build will use these exact patterns. Internalize them here so they feel automatic when you hit Phase 3.

### Before you start this phase, answer these from memory:
1. What is a primary key?
2. What is a foreign key?
3. What does CRUD stand for?
4. Why are parameterized queries safer than string formatting?

If you cannot answer all four, spend 20 minutes reading the SQLite docs introduction before Session 11. The answers are in the CONCEPTS sections below — but attempting recall first makes the reading stick better.

---

# SESSION 11
## SQLite Setup and First Table

---

## CONCEPTS

### 11.1 What SQLite is and why it matters

SQLite is a file-based relational database. Unlike PostgreSQL or MySQL, it requires no server — the entire database is a single `.db` file on disk. This makes it ideal for:
- Development and prototyping
- Small to medium web apps (your portfolio projects qualify)
- Desktop applications
- Anything that does not need concurrent writes from multiple processes

Python's `sqlite3` module is part of the standard library — no installation required.

### 11.2 Connecting and closing

```python
import sqlite3

# Open a connection — creates the file if it does not exist
conn = sqlite3.connect("app.db")

# Set row_factory so rows behave like dicts
conn.row_factory = sqlite3.Row

# Get a cursor — the object you use to run SQL
cursor = conn.cursor()

# Always commit and close when done
conn.commit()
conn.close()
```

`sqlite3.Row` makes each returned row accessible by column name (`row["username"]`) instead of only by index (`row[0]`). Always set this. Index access is fragile — if you change the column order in a query, all your index access breaks.

The `with` statement works with connections too:

```python
with sqlite3.connect("app.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # conn.commit() is called automatically on clean exit
    # conn.rollback() is called automatically on exception
```

### 11.3 Creating a table

```python
def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            created   TEXT    NOT NULL DEFAULT (date('now'))
        )
    """)
    conn.commit()
```

**Key constraints:**

| Constraint | Meaning |
|---|---|
| `PRIMARY KEY` | Uniquely identifies each row. SQLite requires every table to have one. |
| `AUTOINCREMENT` | SQLite auto-assigns the next integer. You never insert this column. |
| `NOT NULL` | This column must always have a value. INSERT fails without it. |
| `UNIQUE` | No two rows can have the same value in this column. |
| `DEFAULT value` | Used when no value is provided on INSERT. |

### 11.4 `CREATE TABLE IF NOT EXISTS`

This makes your initialization idempotent — safe to run multiple times without error or data loss. Always use it. Never use bare `CREATE TABLE` in an init script, because re-running the script would crash.

```python
# BAD — crashes if the table already exists
conn.execute("CREATE TABLE users (...)")

# GOOD — safe to run repeatedly
conn.execute("CREATE TABLE IF NOT EXISTS users (...)")
```

### 11.5 The init script pattern

Your database initialization should be a function called exactly once when the application starts. It creates the database file and all tables if they do not exist. If everything already exists, it does nothing.

```python
def init_db() -> None:
    with sqlite3.connect("app.db") as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        """)
        conn.commit()

# At the bottom of your app file or in __main__:
init_db()
```

### 11.6 SQLite data types

SQLite uses five storage classes, but you mostly care about three:

| SQLite type | Python equivalent | Use for |
|---|---|---|
| `INTEGER` | `int` | IDs, counts, flags (0/1 for booleans) |
| `TEXT` | `str` | Names, passwords, dates as strings |
| `REAL` | `float` | Decimal numbers |

SQLite does not have a native BOOLEAN type. Use `INTEGER` with values 0 and 1. Python's `sqlite3` module converts these automatically when you use `True`/`False` in queries.

SQLite does not have a native DATE type either. Store dates as `TEXT` in ISO format (`"2024-05-01"`) — they sort correctly as strings.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What does `conn.row_factory = sqlite3.Row` do, and why should you always set it?

**Answer:** It changes the type of objects returned by queries from plain tuples to `sqlite3.Row` objects, which support both index access (`row[0]`) and column-name access (`row["username"]`). You should always set it because column-name access is far more readable and not fragile to column order changes in your queries. Without it, you must remember that the username is column 0, password is column 1, etc. — which breaks silently if you ever reorder your SELECT columns.

---

**Question 2:** What is the difference between `PRIMARY KEY` and `UNIQUE`?

**Answer:** Every table has exactly one `PRIMARY KEY` — it is the canonical identifier for each row. It is always unique and never null. A table can have multiple `UNIQUE` constraints on other columns. For example, a users table might have `user_id` as the primary key and `username` as unique — two different users cannot have the same username, but `username` is not the primary key used to reference this row from other tables.

---

**Question 3:** What does `AUTOINCREMENT` do, and what happens if you omit it from a `PRIMARY KEY INTEGER` column?

**Answer:** `AUTOINCREMENT` guarantees that the auto-assigned ID is always higher than any previously used ID, even if rows have been deleted. Without `AUTOINCREMENT`, SQLite will reuse the IDs of deleted rows (it uses `max(id) + 1`). For most applications the difference does not matter. Some applications require that IDs are never reused (audit trails, external references) — those need `AUTOINCREMENT`.

---

**Question 4:** Why is your init script safe to run multiple times when it uses `CREATE TABLE IF NOT EXISTS` but not when it uses `CREATE TABLE`?

**Answer:** `CREATE TABLE` raises an `OperationalError` if the table already exists. `CREATE TABLE IF NOT EXISTS` checks first and does nothing if the table already exists. This matters because your app calls `init_db()` every time it starts. On first run, the tables are created. On subsequent runs, they already exist — the `IF NOT EXISTS` prevents the crash.

---

**Question 5:** You want to store whether a user has verified their email. SQLite has no BOOLEAN type. How do you store this, and how do you read it back in Python?

**Answer:** Store it as `INTEGER NOT NULL DEFAULT 0`. Use 0 for False and 1 for True. When inserting, use Python `True`/`False` — `sqlite3` converts them. When reading, `sqlite3.Row` returns 0 or 1 as integers. In Python, `if row["email_verified"]:` works correctly because `0` is falsy and `1` is truthy. Alternatively, cast explicitly: `bool(row["email_verified"])`.

---

## BUILD TASK

Build `db_init.py`:

**Schema to implement:**

```
Table: users
- user_id   INTEGER PRIMARY KEY AUTOINCREMENT
- username  TEXT NOT NULL UNIQUE
- password  TEXT NOT NULL
- created   TEXT NOT NULL DEFAULT (date('now'))

Table: characters
- char_id       INTEGER PRIMARY KEY AUTOINCREMENT
- user_id       INTEGER NOT NULL
- name          TEXT NOT NULL
- level         INTEGER NOT NULL DEFAULT 1
- weapon_level  INTEGER NOT NULL DEFAULT 1
- FOREIGN KEY (user_id) REFERENCES users (user_id)
```

**Requirements:**
- `init_db()` function — creates both tables using `IF NOT EXISTS`
- Running the script 3 times in a row should not error or alter data
- Print "Database initialized." when done
- Add `users.db` to your `.gitignore`

**Verify:** Run `python db_init.py` three times. Each time it should print the message and exit cleanly. Open the file in a SQLite viewer (DB Browser for SQLite is free) and confirm both tables exist with the correct columns.

---

## SESSION SELF-TEST

1. "I always set `conn.row_factory = sqlite3.Row` because..."
2. "The difference between `PRIMARY KEY` and `UNIQUE` is..."
3. Describe your schema in plain English without reading the code. "The users table stores... The characters table stores... They are related by..."

---

# SESSION 12
## Insert and Read — Parameterized Queries Only

---

## CONCEPTS

### 12.1 Why parameterized queries are non-negotiable

A parameterized query separates the SQL structure from the data values. The database driver handles escaping — you never interpolate user data into SQL strings.

```python
# DANGEROUS — SQL injection vulnerability
username = input("Username: ")
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# What if the user types:  ' OR '1'='1
# The query becomes: SELECT * FROM users WHERE username = '' OR '1'='1'
# This returns ALL users — a complete authentication bypass.

# SAFE — parameterized
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

The `?` is a placeholder. SQLite replaces it with the value safely, escaping any special characters. This is not optional — it is a security requirement.

**Always use `?` placeholders. Never use f-strings or `.format()` in SQL.**

### 12.2 INSERT

```python
def insert_user(conn: sqlite3.Connection, username: str, password: str) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    return cursor.lastrowid   # the auto-assigned ID of the new row
```

`cursor.lastrowid` gives you the `AUTOINCREMENT` ID assigned to the row you just inserted. This is useful when you immediately need to insert related rows referencing this ID.

**Note the tuple:** `(username, password)` — always a tuple, even for one value: `(value,)`. A single-element tuple requires the trailing comma. `(value)` without the comma is just parentheses around `value`, not a tuple.

```python
# WRONG — this is a string, not a tuple
cursor.execute("SELECT * FROM users WHERE username = ?", (username))

# CORRECT — trailing comma makes it a tuple
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### 12.3 SELECT — fetching rows

```python
def get_all_users(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY username")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_user_by_username(conn: sqlite3.Connection, username: str) -> dict | None:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    return dict(row) if row else None
```

**Three fetch methods:**

| Method | Returns | Use when |
|---|---|---|
| `fetchone()` | One row or `None` | You expect 0 or 1 result (login, find by ID) |
| `fetchall()` | List of all rows | You need all results at once |
| `fetchmany(n)` | List of n rows | Pagination (rare in small apps) |

`dict(row)` converts a `sqlite3.Row` to a plain Python dict. Do this when you need to pass the data around — `sqlite3.Row` objects close when the cursor closes.

### 12.4 Handling UNIQUE constraint violations

When you try to insert a duplicate username, SQLite raises `sqlite3.IntegrityError`. Catch it specifically:

```python
def insert_user(conn: sqlite3.Connection, username: str, password: str) -> int | None:
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None   # username already taken
```

### 12.5 Passing the connection around

Notice that every function takes `conn` as its first argument. This is the correct pattern — you create one connection per request (or per session in a CLI app) and pass it to every function that needs it. This avoids global state and makes functions testable.

```python
# Good pattern — connection passed explicitly
def main():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    
    insert_user(conn, "alice", "hashed_pw")
    users = get_all_users(conn)
    for u in users:
        print(u["username"])
    
    conn.close()
```

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is SQL injection, and how do parameterized queries prevent it?

**Answer:** SQL injection is an attack where a malicious user crafts input that changes the structure of a SQL query. For example, if you build a query with `f"WHERE username = '{username}'"` and the user enters `' OR '1'='1`, the query becomes `WHERE username = '' OR '1'='1'` — which returns all users. Parameterized queries prevent this by sending the SQL structure and the data values separately to the database engine. The engine treats the parameter value as pure data, never as SQL syntax, regardless of what characters it contains.

---

**Question 2:** What does `cursor.lastrowid` return, and when is it useful?

**Answer:** `cursor.lastrowid` returns the `AUTOINCREMENT` integer ID of the most recently inserted row. It is useful when you need to immediately insert a related row in another table that references this ID. For example: insert a user, get their `user_id`, then insert a profile row with that `user_id` as a foreign key.

---

**Question 3:** What is the difference between `fetchone()` and `fetchall()`?

**Answer:** `fetchone()` returns the first matching row as a `sqlite3.Row` object, or `None` if no rows matched. Use it when you expect at most one result — login lookup by username, find by ID. `fetchall()` returns a list of all matching rows. Use it when you need all results — listing all items, displaying a table. Using `fetchall()` on a large table loads everything into memory at once; for large datasets prefer iterating the cursor directly.

---

**Question 4:** Why does a single-value parameter tuple require a trailing comma: `(value,)` instead of `(value)`?

**Answer:** In Python, parentheses alone do not create a tuple — they are just grouping. `(value)` is identical to `value`. A trailing comma is what makes something a tuple: `(value,)` is a one-element tuple. The `sqlite3` module requires a sequence (list or tuple) for parameters. Passing `(value)` passes the value itself, which for a string means sqlite3 iterates over the characters of the string and tries to use each character as a parameter — causing an error.

---

**Question 5:** You run this code and get `None` back. What are the two possible reasons?

```python
user = get_user_by_username(conn, "alice")
```

**Answer:** Either (1) no row in the users table has `username = 'alice'` — the user does not exist, or (2) the function explicitly returns `None` when `fetchone()` returns `None`. Both mean the same thing in practice: that username was not found. The caller should check `if user is None:` and handle the "user not found" case.

---

## BUILD TASK

Build `db_crud.py` with these functions. Use the schema from Session 11.

**Functions to implement:**

```python
def insert_user(conn, username: str, hashed_password: str) -> int | None:
    """Insert a user. Return new user_id or None if username taken."""

def get_user_by_username(conn, username: str) -> dict | None:
    """Return user dict or None if not found."""

def get_user_by_id(conn, user_id: int) -> dict | None:
    """Return user dict or None if not found."""

def get_all_users(conn) -> list[dict]:
    """Return all users ordered by username."""

def insert_character(conn, user_id: int, name: str, level: int = 1, weapon_level: int = 1) -> int:
    """Insert a character. Return new char_id."""

def get_characters_for_user(conn, user_id: int) -> list[dict]:
    """Return all characters belonging to user_id."""
```

**Test script (write this in the same file under `if __name__ == "__main__"`):**
```python
init_db()  # import from db_init.py

with sqlite3.connect("app.db") as conn:
    conn.row_factory = sqlite3.Row
    
    # Insert 2 users
    id1 = insert_user(conn, "alice", "fake_hash_1")
    id2 = insert_user(conn, "bob",   "fake_hash_2")
    print(f"Inserted users: {id1}, {id2}")
    
    # Try duplicate
    dup = insert_user(conn, "alice", "another_hash")
    print(f"Duplicate result: {dup}")  # should print None
    
    # Insert characters for alice
    insert_character(conn, id1, "Diluc", level=90)
    insert_character(conn, id1, "Hu Tao", level=80)
    insert_character(conn, id2, "Raiden", level=90)
    
    # Fetch and print
    print("\nAll users:")
    for u in get_all_users(conn):
        print(f"  {u['username']} (id={u['user_id']})")
    
    print("\nAlice's characters:")
    for c in get_characters_for_user(conn, id1):
        print(f"  {c['name']} lv{c['level']}")
    
    print("\nBob's characters:")
    for c in get_characters_for_user(conn, id2):
        print(f"  {c['name']} lv{c['level']}")
```

**Expected output:**
```
Inserted users: 1, 2
Duplicate result: None

All users:
  alice (id=1)
  bob (id=2)

Alice's characters:
  Diluc lv90
  Hu Tao lv80

Bob's characters:
  Raiden lv90
```

---

## SESSION SELF-TEST

1. Write a parameterized INSERT query for a `todos` table with columns `user_id`, `title`, `active`. Do it from memory before checking.
2. "I never use f-strings in SQL queries because..."
3. "The difference between `fetchone()` and `fetchall()` is..."

---

# SESSION 13
## Update, Delete, and Missing ID Handling

---

## CONCEPTS

### 13.1 UPDATE

```python
def update_character_level(
    conn: sqlite3.Connection,
    char_id: int,
    new_level: int
) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE characters SET level = ? WHERE char_id = ?",
        (new_level, char_id)
    )
    conn.commit()
    return cursor.rowcount > 0   # True if a row was actually updated
```

`cursor.rowcount` tells you how many rows were affected by the last `UPDATE` or `DELETE`. If `rowcount` is 0, no rows matched the `WHERE` clause — the ID did not exist. Always check `rowcount` for update and delete operations.

### 13.2 UPDATE multiple columns

```python
def update_character(
    conn: sqlite3.Connection,
    char_id: int,
    name: str,
    level: int,
    weapon_level: int
) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE characters
        SET name = ?, level = ?, weapon_level = ?
        WHERE char_id = ?
        """,
        (name, level, weapon_level, char_id)
    )
    conn.commit()
    return cursor.rowcount > 0
```

Note the parameter order: the `WHERE char_id = ?` placeholder comes last in the SQL, so `char_id` comes last in the tuple.

### 13.3 DELETE

```python
def delete_character(conn: sqlite3.Connection, char_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM characters WHERE char_id = ?",
        (char_id,)
    )
    conn.commit()
    return cursor.rowcount > 0
```

### 13.4 Handling the missing ID case gracefully

```python
def handle_update(conn, char_id: int, new_level: int) -> None:
    success = update_character_level(conn, char_id, new_level)
    if success:
        print(f"Character {char_id} updated to level {new_level}.")
    else:
        print(f"No character found with ID {char_id}.")
```

This pattern — return a boolean from DB helpers, check in the caller — is clean and testable. The DB helper does not print anything. The caller decides what to communicate to the user.

### 13.5 Transactions — why `commit()` matters

SQLite uses transactions. A transaction groups one or more operations into an atomic unit — either all succeed or none do. `conn.commit()` finalizes the transaction, writing changes permanently to disk. `conn.rollback()` undoes all changes since the last commit.

Until you call `commit()`, your changes exist only in memory. If the process crashes before `commit()`, the changes are lost. This is a feature, not a bug — it protects your data from partial writes.

```python
def transfer_character(conn, from_user_id: int, to_user_id: int, char_id: int) -> bool:
    """Move a character from one user to another atomically."""
    try:
        cursor = conn.cursor()
        # Verify ownership
        cursor.execute(
            "SELECT char_id FROM characters WHERE char_id = ? AND user_id = ?",
            (char_id, from_user_id)
        )
        if not cursor.fetchone():
            return False
        # Transfer
        cursor.execute(
            "UPDATE characters SET user_id = ? WHERE char_id = ?",
            (to_user_id, char_id)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        conn.rollback()
        return False
```

### 13.6 Checking ownership before update/delete

When your app has users, always verify that the item being modified belongs to the current user before updating or deleting it.

```python
def delete_character_for_user(
    conn: sqlite3.Connection,
    char_id: int,
    user_id: int
) -> bool:
    """Delete a character only if it belongs to user_id."""
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM characters WHERE char_id = ? AND user_id = ?",
        (char_id, user_id)
    )
    conn.commit()
    return cursor.rowcount > 0
```

By including `AND user_id = ?` in the WHERE clause, you prevent one user from deleting another user's data — even if they know the ID. This is the simplest and most robust approach.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** How do you know if an UPDATE affected any rows?

**Answer:** Check `cursor.rowcount` after the execute. If it is 0, the WHERE clause matched nothing — the ID did not exist or the conditions were not met. If it is greater than 0, that many rows were updated. For updates targeting a single row by primary key, you expect either 0 (not found) or 1 (found and updated).

---

**Question 2:** What is a database transaction, and why does it matter?

**Answer:** A transaction is a group of SQL operations treated as a single atomic unit — they all succeed together or none of them are committed. `commit()` makes the changes permanent. `rollback()` undoes all changes back to the last commit. Transactions matter because real operations often involve multiple steps (insert a user, insert their profile, insert their default settings). If one step fails, you want to roll back the others — partial writes corrupt your data.

---

**Question 3:** Why should you include `AND user_id = ?` in a DELETE query rather than just `WHERE char_id = ?`?

**Answer:** Without the ownership check, any authenticated user who knows a character's ID can delete it — even if it belongs to someone else. Including `AND user_id = ?` makes the query only succeed if the character both exists AND belongs to the current user. This is called authorization — you are not just authenticating (who are you?) but also authorizing (are you allowed to do this specific thing?).

---

**Question 4:** What is the parameter order issue with this UPDATE, and how does it cause a bug?

```python
cursor.execute(
    "UPDATE users SET username = ? WHERE user_id = ?",
    (user_id, username)   # <-- is this right?
)
```

**Answer:** The order is reversed. The SQL has `username = ?` first, then `user_id = ?`. The parameters must match that order: `(username, user_id)`. With `(user_id, username)` as written, SQLite sets `username` to the integer user_id and then looks for a row where `user_id` equals the username string — almost certainly finding nothing and silently doing nothing. Always write the parameter tuple in the same order as the `?` placeholders appear left-to-right in the SQL.

---

**Question 5:** A user tries to delete todo item ID 42. Your delete function returns `False`. What are the two possible reasons?

**Answer:** Either (1) no row with `todo_id = 42` exists in the database — it was already deleted or never existed, or (2) a row with `todo_id = 42` exists but belongs to a different user — the ownership check `AND user_id = ?` prevented the deletion. In both cases, `rowcount` is 0. In a web app, both cases should return a 404 or an access denied response depending on which you want to expose to the user (not exposing which case applies can be a security benefit).

---

## BUILD TASK

Add to `db_crud.py`:

```python
def update_character(conn, char_id: int, user_id: int, name: str, level: int, weapon_level: int) -> bool:
    """Update character. Only succeeds if char_id belongs to user_id. Returns True if updated."""

def delete_character(conn, char_id: int, user_id: int) -> bool:
    """Delete character. Only succeeds if char_id belongs to user_id. Returns True if deleted."""

def update_user_password(conn, user_id: int, new_hashed_password: str) -> bool:
    """Update a user's password. Returns True if updated."""
```

**Test script additions:**
```python
# Test update
success = update_character(conn, 1, id1, "Diluc", 90, 90)
print(f"Updated char 1: {success}")   # True

# Test update wrong owner
fail = update_character(conn, 1, id2, "Diluc", 90, 90)
print(f"Wrong owner update: {fail}")   # False

# Test delete
success = delete_character(conn, 2, id1)
print(f"Deleted char 2: {success}")   # True

# Test delete again (already gone)
fail = delete_character(conn, 2, id1)
print(f"Delete again: {fail}")         # False

# Test delete wrong owner
fail = delete_character(conn, 1, id2)
print(f"Wrong owner delete: {fail}")   # False
```

---

## SESSION SELF-TEST

1. "I check `cursor.rowcount` after UPDATE and DELETE because..."
2. "I include `AND user_id = ?` in my delete queries because..."
3. Write a DELETE query that removes a todo by `todo_id` only if it belongs to `user_id`. Do it from memory.

---

# SESSION 14
## Two-Table Schema — Users and Todos

---

## CONCEPTS

### 14.1 Foreign keys — relating tables

A foreign key is a column in one table that references the primary key of another table. It enforces referential integrity — you cannot insert a row that references a non-existent parent row.

```sql
CREATE TABLE IF NOT EXISTS todos (
    todo_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    title      TEXT    NOT NULL,
    active     INTEGER NOT NULL DEFAULT 1,
    created    TEXT    NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
```

**SQLite foreign key note:** SQLite requires you to enable foreign key enforcement explicitly. It is disabled by default for backwards compatibility.

```python
conn.execute("PRAGMA foreign_keys = ON")
```

Run this immediately after opening a connection. Without it, SQLite accepts any integer as a `user_id` even if no matching user exists.

### 14.2 Querying related data — JOIN

A JOIN combines rows from two tables based on a condition.

```python
# Get all todos for a user with their username shown
cursor.execute("""
    SELECT todos.todo_id, todos.title, todos.active, users.username
    FROM todos
    JOIN users ON todos.user_id = users.user_id
    WHERE todos.user_id = ?
    ORDER BY todos.created DESC
""", (user_id,))
```

For most of your app's queries, you do not need a JOIN — you already know the `user_id` from the session and query directly:

```python
def get_todos_for_user(conn, user_id: int) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM todos WHERE user_id = ? AND active = 1 ORDER BY created DESC",
        (user_id,)
    )
    return [dict(row) for row in cursor.fetchall()]
```

### 14.3 Counting rows

```python
def count_active_todos(conn, user_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM todos WHERE user_id = ? AND active = 1",
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0]   # COUNT(*) returns a single integer
```

`COUNT(*)` returns the number of rows matching the WHERE clause. The result is a single row with a single column — `row[0]` extracts the integer.

### 14.4 Designing a schema — the questions to ask

Before writing a single `CREATE TABLE` statement, answer these questions:

1. **What are the entities?** (Users, Todos, Characters, Tags...)
2. **What data does each entity need?** (name, created date, status...)
3. **What are the relationships?** (A user HAS MANY todos. A todo BELONGS TO one user.)
4. **What must be unique?** (username, email)
5. **What can never be null?** (username, password, todo title)
6. **What has a sensible default?** (created date, active = 1)

Writing these down before coding prevents schema redesigns later.

### 14.5 The full CRUD pattern for a two-table app

```python
# users table — managed during auth
insert_user(conn, username, hashed_password)
get_user_by_username(conn, username)
get_user_by_id(conn, user_id)

# todos table — managed during main app usage
insert_todo(conn, user_id, title)
get_todos_for_user(conn, user_id)
get_todo_by_id(conn, todo_id, user_id)   # always include user_id
update_todo_title(conn, todo_id, user_id, new_title)
toggle_todo_active(conn, todo_id, user_id)
delete_todo(conn, todo_id, user_id)
```

This is the exact function set you will implement in Flask. Memorize this list.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is a foreign key, and what problem does it solve?

**Answer:** A foreign key is a column that references the primary key of another table. It solves referential integrity — it prevents you from inserting a todo with a `user_id` of 999 if no user with ID 999 exists. It also prevents you from deleting a user who still has todos (unless you set `ON DELETE CASCADE`). Without foreign keys, your data can get into inconsistent states where todo rows reference users that no longer exist.

---

**Question 2:** Why does SQLite disable foreign key enforcement by default, and what do you need to do to enable it?

**Answer:** SQLite disables it by default for backwards compatibility — older code and databases would break if foreign key enforcement suddenly became active. To enable it per connection: `conn.execute("PRAGMA foreign_keys = ON")`. This must be run on every new connection — it is not stored in the database file. Add it immediately after `conn = sqlite3.connect(...)` in your connection setup function.

---

**Question 3:** What does `COUNT(*)` return and why do you access it with `row[0]`?

**Answer:** `COUNT(*)` is an aggregate function that returns the number of rows matching the query. The result is a single row containing a single integer. Even with `conn.row_factory = sqlite3.Row`, you access it by index `row[0]` because `COUNT(*)` creates an anonymous column with no natural name (though you can alias it: `SELECT COUNT(*) AS total` and then access `row["total"]`).

---

**Question 4:** Design a schema for a simple note-taking app. Users can have many notes. Each note has a title and body. Write the two CREATE TABLE statements.

**Answer:**
```sql
CREATE TABLE IF NOT EXISTS users (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT    NOT NULL UNIQUE,
    password  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    note_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    title     TEXT    NOT NULL,
    body      TEXT    NOT NULL DEFAULT '',
    created   TEXT    NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

---

**Question 5:** You have this query:

```python
cursor.execute(
    "SELECT * FROM todos WHERE user_id = ?",
    (user_id,)
)
```

A colleague says you should add `AND active = 1`. When would you, and when would you not?

**Answer:** Add `AND active = 1` when you want to show only active todos — like the main todo list view. Omit it when you need all todos regardless of status — like an admin view, a count of total todos ever created, or a "completed todos" view where you want `active = 0`. The right filter depends on the business requirement. Having a separate query function per use case (e.g., `get_active_todos` and `get_all_todos`) is cleaner than adding a boolean parameter to one function.

---

## BUILD TASK

Build `db_todos.py` — a complete set of todo CRUD helpers using the users + todos schema:

**Schema (add to `db_init.py`):**
```sql
CREATE TABLE IF NOT EXISTS todos (
    todo_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL,
    title    TEXT    NOT NULL,
    active   INTEGER NOT NULL DEFAULT 1,
    created  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
```

**Functions to implement:**
```python
def insert_todo(conn, user_id: int, title: str) -> int
def get_todos_for_user(conn, user_id: int, active_only: bool = True) -> list[dict]
def get_todo_by_id(conn, todo_id: int, user_id: int) -> dict | None
def update_todo_title(conn, todo_id: int, user_id: int, new_title: str) -> bool
def toggle_todo_active(conn, todo_id: int, user_id: int) -> bool
def delete_todo(conn, todo_id: int, user_id: int) -> bool
def count_todos(conn, user_id: int, active_only: bool = True) -> int
```

**Test every function.** Include tests for the failure cases: wrong user_id, missing todo_id, toggling an inactive todo back to active.

---

## SESSION SELF-TEST

1. "A foreign key prevents..."
2. "I always include `user_id` in my update and delete queries because..."
3. From memory: write `get_todos_for_user`. Include the `active_only` parameter logic.

---

# SESSION 15
## SQLite Checkpoint — Replace JSON Tracker with SQLite

---

## CONCEPTS

### 15.1 Migrating from JSON to SQLite

Replacing a JSON file with SQLite is a common real-world task. The API your app sees should barely change — only the persistence layer changes.

**Before (JSON):**
```python
def load_items() -> list:
    try:
        with open("tracker.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_items(items: list) -> None:
    with open("tracker.json", "w") as f:
        json.dump(items, f, indent=2)
```

**After (SQLite):**
```python
def get_all_items(conn) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items ORDER BY created")
    return [dict(row) for row in cursor.fetchall()]

def insert_item(conn, text: str) -> int:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (text) VALUES (?)", (text,))
    conn.commit()
    return cursor.lastrowid
```

The calling code changes minimally — it passes a connection instead of a file path, and gets back dicts instead of raw strings. The menu loop and display logic do not need to change at all.

### 15.2 Centralizing DB helpers

All database functions belong in one file. No SQL anywhere else in the app.

```
tracker_v3/
├── main.py          # menu loop, display, user input only
├── db.py            # ALL SQL — init, CRUD helpers
└── tracker.db       # the database file (in .gitignore)
```

`main.py` imports from `db.py`. `main.py` never writes a SQL string. If you find yourself writing `cursor.execute(...)` in `main.py`, stop and move it to `db.py`.

### 15.3 Connection management in a CLI app

For a CLI app, open one connection when the app starts, pass it everywhere, close it when the app exits:

```python
def main():
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    
    db.init(conn)   # create tables if needed
    
    try:
        run_menu(conn)
    finally:
        conn.close()   # always close, even if an exception occurs
```

The `try/finally` ensures the connection closes even if the app crashes. In Flask you will manage connections differently (per-request), but for CLI apps this is correct.

### 15.4 What you can now do from memory

By the end of this session, you should be able to reproduce this entire pattern from scratch:

```python
import sqlite3

def get_connection(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(conn) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            text     TEXT    NOT NULL,
            done     INTEGER NOT NULL DEFAULT 0,
            created  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

def insert_item(conn, text: str) -> int:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (text) VALUES (?)", (text,))
    conn.commit()
    return cursor.lastrowid

def get_all_items(conn) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items ORDER BY created")
    return [dict(row) for row in cursor.fetchall()]

def toggle_done(conn, item_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET done = 1 - done WHERE item_id = ?",
        (item_id,)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_item(conn, item_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0
```

Note the `1 - done` trick for toggling a boolean integer: `1 - 0 = 1`, `1 - 1 = 0`. A clean one-liner for toggling.

---

## CHECK YOUR UNDERSTANDING

**Question 1:** What is the `1 - done` trick and why does it work for toggling a boolean column?

**Answer:** SQLite stores booleans as integers (0 = false, 1 = true). `1 - 0 = 1` and `1 - 1 = 0`. So `UPDATE items SET done = 1 - done` flips the value without any conditional logic or fetching the current value first. It is atomic — the read and write happen in a single SQL statement.

---

**Question 2:** Where should all SQL statements live in your app, and why?

**Answer:** All SQL belongs in one dedicated file (commonly `db.py` or `database.py`). No SQL should appear in `main.py`, route handlers, or anywhere else. This is the separation of concerns principle applied to data access. When you need to change a query, you know exactly where to look. When testing, you can test the DB layer independently. When switching databases (e.g., from SQLite to PostgreSQL), you only change one file.

---

**Question 3:** Why use `try/finally` when managing a database connection in a CLI app?

**Answer:** `finally` runs regardless of whether an exception was raised. Without it, if the menu loop raises an unhandled exception, `conn.close()` is never called. The connection stays open until the OS cleans it up, and any uncommitted changes may be lost. `try/finally` guarantees the cleanup runs no matter what.

---

**Question 4:** Compare the JSON and SQLite approaches for a tracker app. Name one advantage of each.

**Answer:** JSON advantage: simpler to set up — no schema, just read and write a file. Good for tiny apps or configuration storage. SQLite advantage: enforces data types and constraints, supports concurrent queries efficiently, scales to thousands of rows without loading everything into memory, supports filtering and sorting at the database level rather than in Python. For any app with structured data and relationships, SQLite is the better choice.

---

**Question 5:** Write the `get_connection` function from memory. Include all three required setup lines.

**Answer:**
```python
import sqlite3

def get_connection(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
```

The three required lines are: connect to the file, set `row_factory`, enable foreign keys. Many developers forget the third line — SQLite's foreign key enforcement is off by default.

---

## BUILD TASK

Rebuild `tracker_v2.py` as `tracker_v3/` — a package with proper structure:

```
tracker_v3/
├── db.py       # all SQL
└── main.py     # all UI
```

**`db.py` must contain:**
- `get_connection(path)` — connect, set row_factory, enable foreign keys
- `init_db(conn)` — create items table
- `insert_item(conn, text)` → int
- `get_all_items(conn)` → list[dict]
- `toggle_done(conn, item_id)` → bool
- `delete_item(conn, item_id)` → bool
- `count_items(conn, done_only=False)` → int

**`main.py` must contain:**
- Menu loop: Add / View / Toggle Done / Delete / Counts / Exit
- Display shows index, done status, and item text
- No SQL anywhere in this file

**Done means:**
- Add 3 items
- Toggle one as done
- Exit and reopen — all state persists including done status
- Delete by index with a message for invalid indexes
- `count_items` reports active and done counts separately

---

## REBUILD FROM MEMORY CHECK

Before committing this session's work, close everything and write the following from memory on paper or in a scratch file. No peeking.

1. The `get_connection` function
2. A `CREATE TABLE IF NOT EXISTS` statement with at least 4 columns including a primary key
3. A parameterized `INSERT` statement with `cursor.lastrowid`
4. A `SELECT *` with a `WHERE` clause and `fetchall()`
5. An `UPDATE` with `cursor.rowcount` check
6. A `DELETE` with ownership check (`AND user_id = ?`)

If you can write all six from memory, you are ready for Phase 3.
If not, identify the gaps and spend 20 minutes on them before moving to Session 16.

---

## SESSION SELF-TEST

1. "The six SQL operations I need to know from memory are..."
2. "No SQL belongs in `main.py` because..."
3. "After opening a SQLite connection, the two things I always do immediately are..."

---

# PHASE 2 SKILL CHECKPOINT

Rate yourself honestly before starting Phase 3.

| Skill | Rating (1–5) | What I still need to practice |
|---|---|---|
| Write `CREATE TABLE IF NOT EXISTS` from memory | | |
| Write a parameterized INSERT from memory | | |
| Write a SELECT with WHERE from memory | | |
| Write an UPDATE with rowcount check from memory | | |
| Write a DELETE with ownership check from memory | | |
| Explain what a foreign key does | | |
| Explain why string formatting in SQL is dangerous | | |
| Set up a connection correctly (row_factory + foreign_keys) | | |
| Centralize all SQL in one file | | |

**Minimum to proceed:** All ratings 3 or above. Any rating below 3 means re-do that session's build task before continuing.

---

# PHASE 2 REFERENCE SHEET
## SQLite Patterns — Reproduce from Memory

```python
import sqlite3

# ── Connection ──────────────────────────────────────────
def get_connection(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ── Init ────────────────────────────────────────────────
def init_db(conn) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text    TEXT    NOT NULL,
            done    INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    conn.commit()

# ── Insert ──────────────────────────────────────────────
def insert_item(conn, user_id: int, text: str) -> int:
    c = conn.cursor()
    c.execute(
        "INSERT INTO items (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )
    conn.commit()
    return c.lastrowid

# ── Select ──────────────────────────────────────────────
def get_items(conn, user_id: int) -> list[dict]:
    c = conn.cursor()
    c.execute(
        "SELECT * FROM items WHERE user_id = ? ORDER BY item_id",
        (user_id,)
    )
    return [dict(row) for row in c.fetchall()]

def get_item(conn, item_id: int, user_id: int) -> dict | None:
    c = conn.cursor()
    c.execute(
        "SELECT * FROM items WHERE item_id = ? AND user_id = ?",
        (item_id, user_id)
    )
    row = c.fetchone()
    return dict(row) if row else None

# ── Update ──────────────────────────────────────────────
def update_item(conn, item_id: int, user_id: int, text: str) -> bool:
    c = conn.cursor()
    c.execute(
        "UPDATE items SET text = ? WHERE item_id = ? AND user_id = ?",
        (text, item_id, user_id)
    )
    conn.commit()
    return c.rowcount > 0

def toggle_done(conn, item_id: int, user_id: int) -> bool:
    c = conn.cursor()
    c.execute(
        "UPDATE items SET done = 1 - done WHERE item_id = ? AND user_id = ?",
        (item_id, user_id)
    )
    conn.commit()
    return c.rowcount > 0

# ── Delete ──────────────────────────────────────────────
def delete_item(conn, item_id: int, user_id: int) -> bool:
    c = conn.cursor()
    c.execute(
        "DELETE FROM items WHERE item_id = ? AND user_id = ?",
        (item_id, user_id)
    )
    conn.commit()
    return c.rowcount > 0

# ── Count ────────────────────────────────────────────────
def count_items(conn, user_id: int) -> int:
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM items WHERE user_id = ?",
        (user_id,)
    )
    return c.fetchone()[0]
```

**This reference sheet exists for you to use during Phase 3 if you get stuck.
Your goal by the end of Phase 3 is to not need it.**
