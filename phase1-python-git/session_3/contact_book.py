### TODO
# # load and save contacts to a persistent JSON storage
# save function
# load function

# # Add contacts
# List contacts
# find contact
# remove contact

import json
from pathlib import Path

from typing import Callable, TypedDict
from collections.abc import Mapping


class MenuEntry(TypedDict):
    label : str
    command : Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


#  Learned from phase1 workbook - tried finding docs breifly but could only find general stack
# overflow questions and answers that confirmed usage
script_dir = Path(__file__).resolve().parent # needs additional learning
SAVE_FILE = script_dir / "contacts.json"

def save_contacts(contact_list: list, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(contact_list, f, indent=2)

def load_contacts(path: str) -> list:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # first run - no file - return empty object
    except json.JSONDecodeError:
        print("Warning: File could not be read, loading blank contacts.")
        return [] # return empty contact list object if file reads corrupt 

def clean_text(text: str) -> str:
    return " ".join(text.split()).title()


def get_safe_input(prompt: str) -> str | None:
    user_input = clean_text(input(prompt))
    if not user_input:
        return None
    return user_input

def get_non_empty(prompt: str) -> str:
    while True:
        user_input = get_safe_input(prompt)
        if user_input is None:
            print("Entry was empty, please try again.")
            continue
        return user_input
        

def show_menu(menu: MenuDict):
    print()
    for i, entry in menu.items():
        print(f"{i}.) {entry['label']}")
    print()


def handle_menu_input(prompt: str, menu: MenuDict) -> None:
    user_input = get_non_empty(prompt)
    menu_item = menu.get(user_input)

    if menu_item is not None:
        menu_item["command"]()
    else:
        print("Invalid menu option")


def main() -> None:
    running = True
    contacts = load_contacts(SAVE_FILE)

    def add_contact():
        pass
                

    def list_contact():
        print(contacts)


    def find_contact():
        pass


    def delete_contact():
        pass


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