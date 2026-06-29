from pathlib import Path
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


def insert_todo() -> None:
    pass


def get_todos_for_user() -> None:
    pass


def get_todo_by_id() -> None:
    pass


def update_todo_title() -> None:
    pass


def toggle_todo_active() -> None:
    pass


def delete_todo() -> None:
    pass


def count_todos() -> None:
    pass


def main() -> None:
    __init__(master_database)


if __name__ == "__main__":
    main()