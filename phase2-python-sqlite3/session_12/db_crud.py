from pathlib import Path
from typing import Any
import sqlite3

absolute_path = Path(__file__).parent
master_database = absolute_path / 'characters.db'

def connect_execute_db_close(path: Path, command: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(command, params)
        conn.commit()
        result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result


def init(path: Path) -> None:
    connect_execute_db_close(path, """
                            CREATE TABLE IF NOT EXISTS users(
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                                password TEXT NOT NULL
                            )"""
    )
    connect_execute_db_close(path, """
                            CREATE TABLE IF NOT EXISTS characters(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                name TEXT UNIQUE NOT NULL,
                                level INTEGER NOT NULL DEFAULT 1,
                                auto_level INTEGER NOT NULL DEFAULT 1,
                                skill_level INTEGER NOT NULL DEFAULT 1,
                                burst_level INTEGER NOT NULL DEFAULT 1,
                                constellations INTEGER NOT NULL DEFAULT 1,
                                FOREIGN KEY (user_id) REFERENCES users (user_id)
                            )"""
    )
    connect_execute_db_close(path,"""
                            CREATE TABLE IF NOT EXISTS weapons(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                level INTEGER NOT NULL DEFAULT 1,
                                refinement INTEGER NOT NULL DEFAULT 1,
                                FOREIGN KEY (user_id) REFERENCES users (user_id)
                            )"""
    
    )




def insert_user(path: Path, username: str, password: str) -> None:
    try:
        connect_execute_db_close(path, """
            INSERT INTO users (username, password) VALUES (?, ?)
            """, (username, password)
        )
        print(f"Successfully registered {username}")
    except sqlite3.IntegrityError:
        print(f"Sorry, the username {username} is already taken, please try again.")


def remove_password(user: dict[str, Any]) -> dict[str, Any]:
    user.pop('password', None)
    return user


def get_user_by_username(path: Path, username: str) -> dict[str, Any] | None:
    user = connect_execute_db_close(path, """
        SELECT * FROM users WHERE username = ?                           
        """, (username,)
    )
    return remove_password(user[0]) if user else None


def get_user_by_id(path: Path, user_id: int) -> dict[str, Any] | None:
    user = connect_execute_db_close(path, """
        SELECT * FROM users WHERE user_id = ?
        """, (user_id,)
    )
    return remove_password(user[0]) if user else None


def get_all_users(path: Path) -> list[dict[str, Any]] | None:
    users = connect_execute_db_close(path, """
        SELECT * FROM users ORDER BY username
        """
    )
    if users:
        users = [remove_password(user) for user in users]
        return users
    else:
        return None


def insert_character(path: Path, 
                     user_id: int,
                     name: str,
                     level: int = 1, 
                     auto_level: int = 1, 
                     skill_level: int = 1, 
                     burst_level: int = 1,
                     constellations: int = 1) -> bool:
    try:
        connect_execute_db_close(path, """
            INSERT INTO characters (user_id, name, level, auto_level, skill_level, burst_level, constellations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, name, level, auto_level, skill_level, burst_level, constellations)
        )
        print(f"Successfully added {name}!")
        return True
    except sqlite3.IntegrityError:
        print(f"{name} already exists!")
        return False

def get_characters_for_user(path: Path, user_id: int) -> list[dict[str, Any]] | None:
    characters = connect_execute_db_close(path, """
        SELECT * FROM characters WHERE user_id = ?
        """, (user_id,)
    )
    return characters if characters else None
    


def test() -> None:
    insert_user(master_database, 'bob', 'pass')
    insert_user(master_database, 'bOb', 'pass')
    bo = get_user_by_username(master_database, 'bo')
    bob = get_user_by_username(master_database, 'bob')
    if bob is not None:
        get_user_by_id(master_database, bob['user_id'])
        insert_character(master_database, bob['user_id'], 'Hu tao', 90, constellations=6)
        characters = get_characters_for_user(master_database, bob['user_id'])
        if characters is not None:
            for character in characters:
                print(f"{character['name']}")
    if bo is not None:
        get_user_by_id(master_database, bo['user_id'])
    users = get_all_users(master_database)
    if users is not None:
        for user in users:
            print(f"{user['user_id']}.) {user['username']}")
    

def main() -> None:
    init(master_database)
    test()


if __name__ == "__main__":
    main()