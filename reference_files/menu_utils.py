import validators as val
from typing import Callable, TypedDict
from collections.abc import Mapping

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]

def show_menu(menu: MenuDict) -> None:
    """Displays each menu option and its label"""
    print()
    for index, value in menu.items():
        print(f"{index}.) {value['label']}")
    print()

def handle_input(user_input: str, menu: MenuDict) -> None:
    """Validate menu input and execute the matching command."""
    if not val.is_nonempty(user_input):
        print("Input cannot be blank, please try again")
        return
    
    if user_input in menu:
        menu[user_input]['command']()
    else:
        print("Invalid menu option, please try again")