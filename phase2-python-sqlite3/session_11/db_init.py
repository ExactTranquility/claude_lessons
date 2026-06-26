from pathlib import Path
import sqlite3

absolute_path = Path(__file__).parent
characters_db = absolute_path / "characters.db"

def execute_db(database: Path, command: str) -> None:
    with sqlite3.connect(database) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute(command)
        conn.commit()

def init_characters_db() -> None:
    # create users table so multiple people can use the database w/ login credentials
    execute_db(characters_db, """
        CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
    """)
    # create character table
    execute_db(characters_db, """
            CREATE TABLE IF NOT EXISTS characters(
                char_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                level INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id))
    """)
    # create weapon table
    execute_db(characters_db, """
            CREATE TABLE IF NOT EXISTS weapons(
                weap_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                refinment INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id))
            """)
    print("Database initialized")
    
if __name__ == "__main__":
    for _ in range(0, 3):
        init_characters_db()