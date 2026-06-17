### TODO
# List contacts
# find contact
# remove contact

import json
from pathlib import Path

from typing import Callable, TypedDict, NotRequired
from collections.abc import Mapping


class MenuEntry(TypedDict):
    label : str
    command : Callable[[], None]

MenuDict = Mapping[str, MenuEntry]

class Contact(TypedDict):
    name: str
    phone_number: NotRequired[str]
    email: NotRequired[str]

#  Learned from phase1 workbook - tried finding docs breifly but could only find general stack
# overflow questions and answers that confirmed usage
script_dir = Path(__file__).resolve().parent # needs additional learning
SAVE_FILE = script_dir / "contacts.json"

def save_contacts(contact_list: list[Contact], path: Path) -> None:
    with open(path, 'w') as f:
        json.dump(contact_list, f, indent=2)

def load_contacts(path: Path) -> list[Contact]:
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

    
    def find_contact():
        user_input = get_non_empty("Name of contact : ")
        person = next((contact for contact in contacts if contact.get("name") == user_input), None)
        if person is not None:
            print(person)
            return
        print("That person is not in your contact list")
    

    def add_contact():
        name = get_non_empty("Name of new contact : ")
        phone_number = get_safe_input("Contact phone number (optional) : ")
        email = get_safe_input("Contact email (optional) : ")
        
        contact = Contact(name = name)
        if phone_number is not None:
            contact["phone_number"] = phone_number
        if email is not None:
            contact["email"] = email

        contacts.append(contact)
        
        print("Contact added successfully, returning to main menu.")

             
    
    def list_contact():
        print(contacts)
    

    def delete_contact():
        pass


    def exit_program() -> None:
        nonlocal running
        running = False
    
    
    menu: MenuDict = {
        "1" : {
            "label" : "Search contact",
            "command" : find_contact
        },
        "2" : {
            "label" : "Add new contact",
            "command" : add_contact
        },
        "3" : {
            "label" : "List contacts",
            "command" : list_contact
        },
        "4" : {
            "label" : "Delete contact",
            "command" : delete_contact
        },
        "5" : {
            "label" : "Exit Program",
            "command" : exit_program
        }
    }

    while running:
        show_menu(menu)
        handle_menu_input("Please select a menu option : ", menu)



if __name__ == "__main__":
    main()