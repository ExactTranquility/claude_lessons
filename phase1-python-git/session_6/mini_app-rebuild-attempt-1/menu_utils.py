from typing import Callable, TypedDict 
from collections.abc import Mapping

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


def show_menu(menu: MenuDict) -> None:
    print()
    for i, entry in menu.items():
        print(f"{i}.) {entry['label']}")
    print()


def handle_menu_input(user_input: str, menu: MenuDict) -> bool:
    choice = menu.get(user_input)

    if choice is not None:
        choice['command']()
        return True
    else:
        return False