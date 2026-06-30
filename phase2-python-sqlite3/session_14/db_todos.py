from pathlib import Path
from typing import Any
import sqlite3

absolute_path = Path(__file__).parent
master_database = absolute_path / 'todos.db'


def connect_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def __init__(path: Path) -> None:
    conn = connect_db(path)
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL    UNIQUE  COLLATE NOCASE,
            password    TEXT    NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS todos(
            todo_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title       TEXT    NOT NULL,
            body        TEXT    NOT NULL    DEFAULT '',
            archived    INTEGER NOT NULL    DEFAULT 0,
            created     TEXT    NOT NULL    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (user_id))""")
    finally:
        conn.close()


def insert_user(conn: sqlite3.Connection, username, password) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users
        (username, password)
        VALUES (?, ?)
        """, (username, password))
    conn.commit()
    assert cursor.lastrowid is not None
    return cursor.lastrowid

    

def get_user_id_by_username(conn: sqlite3.Connection, username) -> int:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id FROM users
        WHERE username = ?
        """, (username,))
    return cursor.fetchone()[0]



def insert_todo(conn: sqlite3.Connection, user_id: int, todo_title: str, todo_body:str='') -> int:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO todos
        (user_id, title, body)
        VALUES (?, ?, ?)
        """, (user_id, todo_title, todo_body))
    conn.commit()
    assert cursor.lastrowid is not None
    return cursor.lastrowid


def get_todos_for_user(conn: sqlite3.Connection, user_id: int) -> list[dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM todos
        WHERE user_id = ?
        """, (user_id,))
    
    results = [dict(row) for row in cursor.fetchall()]
    return results

def get_todo_by_id(conn: sqlite3.Connection, todo_id: int, user_id: int) -> dict[str, Any] | None:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM todos
        WHERE todo_id = ?
        AND user_id = ?           
        """, (todo_id, user_id))
    
    result = cursor.fetchone()
    if result is not None:
        return dict(result)
    return None


def update_todo_title(conn: sqlite3.Connection, todo_id: int, user_id: int, new_title: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE todos
        SET title = ?
        WHERE todo_id = ?
        AND user_id = ?
        """, (new_title, todo_id, user_id))
    conn.commit()
    return cursor.rowcount > 0


def toggle_todo_active(conn: sqlite3.Connection, todo_id: int, user_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE todos
        SET archived = CASE WHEN ARCHIVED = 1 THEN 0 ELSE 1 END
        WHERE todo_id = ?
        AND user_id = ?
        """, (todo_id, user_id))
    conn.commit()
    return cursor.rowcount > 0


def delete_todo(conn: sqlite3.Connection, todo_id: int, user_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM todos
        WHERE todo_id = ?
        AND user_id = ?
        """, (todo_id, user_id))
    conn.commit()
    return cursor.rowcount > 0


def count_todos(conn: sqlite3.Connection) -> None:
    count = conn.execute("""
        SELECT COUNT(*) FROM todos
        """)
    return count.fetchone()[0]


def test() -> None:
    conn = connect_db(master_database)
    try:
        print(count_todos(conn))
        try:
            insert_user(conn, 'David', 'Password')
        except sqlite3.IntegrityError:
            print("Username already exist")
        david_id = get_user_id_by_username(conn, 'david')
        print(david_id)
        david_todo = insert_todo(conn, david_id, 'Test')
        # print(get_todos_for_user(conn, david_id))
        print(get_todo_by_id(conn, david_todo, david_id))
        update_todo_title(conn, david_todo, david_id, 'Final')
        print(get_todo_by_id(conn, david_todo, david_id))
        toggle_todo_active(conn, david_todo, david_id)
        print(get_todo_by_id(conn, david_todo, david_id))
        toggle_todo_active(conn, david_todo, david_id)
        print(get_todo_by_id(conn, david_todo, david_id))
        delete_todo(conn, david_todo, david_id)
        print(get_todo_by_id(conn, david_todo, david_id))
        print(count_todos(conn))

    finally:
        conn.close()


def main() -> None:
    __init__(master_database)
    test()


if __name__ == "__main__":
    main()