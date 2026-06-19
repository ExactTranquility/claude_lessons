from typing import Callable, TypedDict
from collections.abc import Mapping

import json
from pathlib import Path

script_dir = Path(__file__).resolve().parent # needs additional learning
SAVE_FILE = script_dir / "item_list.json"

def load_file(path: Path) -> list[str]:
    try:
        with open(path, 'r',) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning!!! File not found at {path}, creating new list")
        return []
    except json.JSONDecodeError:
        print("Warning!!! File was unable to be read, starting with empty list")
        return []
    
def save_file(lst: list[str], path: Path):
    with open(path, 'w') as f:
        json.dump(lst, f, indent=2)

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


items = load_file(SAVE_FILE)


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

def conv_int(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None

def reprompt(reason: str) -> bool:
    user_input = get_safe_input(f"{reason}, do you want to enter a different item? (Y/N) : ")
    return user_input in ["Yes", "Y"]
        

def is_list_empty(lst : list) -> bool:
    if not lst:
        print("The list is empty!")
        return True
    return False
    


def add_item() -> None:
    view_items()
    print()
    while True:
        user_input = get_non_empty("Please enter an item to add to the list: ")
            
        if user_input in items:
            if reprompt(f"{user_input} is already in the list"):
                continue
            
            print("Returning to main menu")
            return
        
        items.append(user_input)
        save_file(items, SAVE_FILE)
        print(f"{user_input} added succesfully, returning to main menu")
        return
                           


def view_items() -> None:
    if is_list_empty(items):
        return
    for i, item in enumerate(items, 1):
        print(f"{i}.) {item}")
    
    
def remove_item_by_name() -> None:
    if is_list_empty(items):
        return
    while True:
        user_input = get_non_empty("Please enter an item to removed from the list: ")
         
        if user_input in items:
            items.remove(user_input)
            save_file(items, SAVE_FILE)
            print(f"{user_input} removed from list, returning to main menu")
            return
            
        if reprompt(f"{user_input} is not in the list"):
            continue
        print("Returning to main menu")
        return

def remove_item_by_index() -> None:
    if is_list_empty(items):
        return
    while True:
        #  Display the list to make selection easier
        view_items()
        print()

        # Get a valid string input that is not empty, then see if it can be converted to an int
        user_input = get_non_empty("Please enter an item to removed from the list: ")
        user_input = conv_int(user_input)

        if user_input is None:
            print("Sorry that was not a valid number, please try again.")
            continue

        #  Since we are displaying 1-based indexing, check if in range of user visible input then convert and remove the item
        if user_input > 0 and user_input <= len(items):
            items.pop(user_input - 1)
            save_file(items, SAVE_FILE)
            print("Item removed sucessfully! Returning to main menu")
        else:
            if reprompt(f"{user_input} is not a valid selection"):
                continue
            
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

        save_file(items, SAVE_FILE)

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
        "command" : remove_item_by_index
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
