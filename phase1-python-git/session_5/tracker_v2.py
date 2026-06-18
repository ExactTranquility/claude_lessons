### TODO
# - add persistence with json
# json load
# json save
# json save on every mutate
# - display the list with index values (1-based)
# - change functionality to remove items by index value
# - check for invalid indexes
# - non-numeric input with error handling


from typing import Callable, TypedDict
from collections.abc import Mapping

import json
from pathlib import Path

script_dir = Path(__file__).resolve().parent # needs additional learning
SAVE_FILE = script_dir / "contacts.json"

def load_file(path: Path) -> list[str]:
    try:
        with open(path, 'r',) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found at {path}, creating new list")
        return []
    except json.JSONDecodeError:
        print("Warning!!! File was unable to be read, starting with empty list")
        return []

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


items = []


def clean_text(text: str) -> str:
    return " ".join(text.strip().split()).title()
    

def get_safe_input(prompt: str) -> str | None:
    user_input = clean_text(input(prompt))
    if not user_input:
        return None
    return user_input


def get_non_empty(prompt: str) -> str:
    while True:
        user_input = clean_text(input(prompt))
        if not user_input:
            print("Entry was empty, please try again.")
            continue
        return user_input


def reprompt(reason: str) -> bool:
    user_input = get_safe_input(f"{reason}, do you want to enter a different item? (Y/N) : ")
    return user_input in ["Yes", "Y"]
        

def is_list_empty(lst : list) -> bool:
    if not lst:
        print("The list is empty!")
        return True
    return False
    


def add_item() -> None:
    while True:
        user_input = get_non_empty("Please enter an item to add to the list: ")
            
        if user_input in items:
            if reprompt(f"{user_input} is already in the list"):
                continue
            
            print("Returning to main menu")
            return
        
        items.append(user_input)
        print(f"{user_input} added succesfully, returning to main menu")
        return
                           


def view_items() -> None:
    if is_list_empty(items):
        return
    for i, item in enumerate(items, 1):
        print(f"{i}.) {item}")
    
    
def remove_item() -> None:
    if is_list_empty(items):
        return
    while True:
        user_input = get_non_empty("Please enter an item to removed from the list: ")
         
        if user_input in items:
            items.remove(user_input)
            print(f"{user_input} removed from list, returning to main menu")
            return
            
        if reprompt(f"{user_input} is not in the list"):
            continue
        print("Returning to main menu")
        return
        
    
def count_items() -> None:
    if is_list_empty(items):
        return
    
    len_of_list = len(items)
    display_s = "item" if len_of_list == 1 else "items"
    print(f"Your list has {len_of_list} {display_s}")
    

def show_menu(menu: MenuDict) -> None:    
    print()
    for index, value in menu.items():
        print(f"{index}.) {value['label']}")
    print()



def main() -> None:
    running = True
    
    def exit_program() -> None:
        nonlocal running
        running = False
    
    menu: MenuDict = {
    "1" : {
        "label" : "Add item",
        "command" : add_item
    },
    "2" : {
        "label" : "View items",
        "command" : view_items
    },
    "3" : {
        "label" : "Remove item",
        "command" : remove_item
    },
    "4" : {
        "label" : "Count items",
        "command" : count_items
    },
    "5" : {
        "label" : "Quit",
        "command" : exit_program
    }
    }
    
    while running:
        show_menu(menu)
        user_input = get_safe_input("Choose a menu option: ")        
        
        if user_input is None:
            print("Input cannot be blank")
            continue

        if user_input in menu:
            menu[user_input]['command']()
        else:
            print("Invalid menu option, please try again")


if __name__ == "__main__":
    main()
