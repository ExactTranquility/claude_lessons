
from typing import Callable, TypedDict
from collections.abc import Mapping


class MenuEntry(TypedDict):
    label : str
    command : Callable[[], None]

MenuDict = Mapping[str, MenuEntry]

def save_contacts():
    pass

def load_contacts():
    pass

def clean_text(text: str) -> str:
    return " ".join(text.split()).strip().title()


def get_clean_text(prompt: str) -> str | None:
    user_input = clean_text(input(prompt))
    if not user_input:
        return None
    return user_input

def get_non_empty(prompt: str) -> str:
    while True:
        user_input = get_clean_text(prompt)
        if user_input is None:
            print("Entry was empty, please try again.")
            continue
        return user_input
        

def show_menu(menu: MenuDict):
    print()
    for i, menu_item in menu.items():
        print(f"{i}.) {menu_item['label']}")
    print()


def handle_menu_input(prompt: str, menu: MenuDict) -> None:
    user_input = get_non_empty(prompt)
    menu_item = menu.get(user_input)

    if menu_item is not None:
        menu_item["command"]()
    else:
        print("Invalid menu option")


def add_contact():
    pass

def list_contact():
    pass

def find_contact():
    pass

def delete_contact():
    pass

def main() -> None:
    running = True

    def exit_program() -> None:
        nonlocal running
        running = False
    
    menu: MenuDict = {
        "1" : {
            "label" : "Add contact",
            "command" : add_contact
        },
        "2" : {
            "label" : "List contacts",
            "command" : list_contact
        },
        "3" : {
            "label" : "Exit Program",
            "command" : exit_program
        }
    }

    while running:
        show_menu(menu)
        handle_menu_input("Please select a menu option : ", menu)



if __name__ == "__main__":
    main()