import json
from pathlib import Path

from typing import Callable, TypedDict, NotRequired, cast
from collections.abc import Mapping

EMPTY_ERROR_MSG = "Your contact list is empty!"


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
            return cast(list[Contact], json.load(f))
    except FileNotFoundError:
        return [] # first run - no file - return empty object
    except json.JSONDecodeError:
        print("Warning: File could not be read, loading blank contacts.")
        return [] # return empty contact list object if file reads corrupt 

def clean_text(text: str) -> str:
    return " ".join(text.split())


def comp_text(text: str, user_input: str) -> bool:
    if text is not None and user_input is not None:
        if text.lower() == user_input.lower():
            return True
    return False


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

    
    def find_contact() -> None:
        if not contacts:
            print(EMPTY_ERROR_MSG)   
            return

        user_input = get_non_empty("Name of contact : ")
        person = next((contact for contact in contacts if comp_text(contact.get("name"), user_input)), None)
        if person is not None:
            for k,v in person.items():
                print(k, v, sep = ' : ')
            return
        print("That person is not in your contact list, returning to main menu.")
    

    def add_contact() -> None:
        name = get_non_empty("Name of new contact : ")
        phone_number = get_safe_input("Contact phone number (optional) : ")
        email = get_safe_input("Contact email (optional) : ")

        contact = Contact(name = name)
        contact["phone_number"] = phone_number if phone_number is not None else "Unknown"
        contact["email"] = email if email is not None else "Unknown"

        contacts.append(contact)
        save_contacts(contacts, SAVE_FILE)
        
        print("Contact added successfully, returning to main menu.")

             
    
    def list_contact() -> None:
        if not contacts:
            print(EMPTY_ERROR_MSG)   
            return  
        print()
        
        contact_list = enumerate(contacts, start = 1)
        for i, contact in contact_list:
            print(f"{i}.) ", end='')
            for k, v in contact.items():
                print(k.capitalize(), v, sep=" : ")
    

    def delete_contact() -> None:
        if not contacts:
            print(EMPTY_ERROR_MSG)
            return
        user_input = get_non_empty("Name of contact to be deleted : ")
        contact = next((contact for contact in contacts if comp_text(contact.get("name"), user_input)), None)
        
        if contact is None:
            print("Contact not found, returning to main menu.")
            return
        contacts.remove(contact)
        save_contacts(contacts, SAVE_FILE)
        print("Contact removed successfully, returning to main menu.")



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