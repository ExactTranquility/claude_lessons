 # # # TODO
 
from pathlib import Path
import sqlite3

absolute_path = Path(__file__).parent
master_database = absolute_path / 'characters.db'

def connect_execute_db_close(path: Path, command_param: tuple) -> list[dict] | None:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(*command_param)
        conn.commit()
        return cursor.fetchall()


def init(path: Path) -> None:
    connect_execute_db_close(path, ("""
                            CREATE TABLE IF NOT EXISTS users(
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL
                            )""",)
    )
    connect_execute_db_close(path, ("""
                            CREATE TABLE IF NOT EXISTS characters(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                name TEXT UNIQUE NOT NULL,
                                level INTEGER NOT NULL DEFAULT 0,
                                auto_level INTEGER NOT NULL DEFAULT 1,
                                skill_level INTEGER NOT NULL DEFAULT 1,
                                burst_level INTEGER NOT NULL DEFAULT 1,
                                constellations INTEGER NOT NULL DEFAULT 1,
                                FOREIGN KEY (user_id) REFERENCES users (user_id)
                            )""",)
    )
    connect_execute_db_close(path,("""
                            CREATE TABLE IF NOT EXISTS weapons(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                level INTEGER NOT NULL DEFAULT 1,
                                refinement INTEGER NOT NULL DEFAULT 1,
                                FOREIGN KEY (user_id) REFERENCES users (user_id)
                            )""",)
    
    )



def insert_user() -> None:
    pass


def get_user_by_username() -> None:
    pass


def get_user_by_id() -> None:
    pass 


def get_all_users() -> None:
    pass


def insert_character() -> None:
    pass


def get_characters_for_user() -> None:
    pass



def main() -> None:
    init(master_database) 


if __name__ == "__main__":
    main()