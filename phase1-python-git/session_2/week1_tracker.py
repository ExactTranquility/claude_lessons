from typing import Callable, TypedDict
from collections.abc import Mapping

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


items = []


def clean_text(text: str) -> str:
    return " ".join(text.strip().split()).capitalize()
    

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
    print(items)
    
    
def remove_item() -> None:
    while True:
        user_input = get_non_empty("Please enter an item to removed from the list: ")
         
        if user_input in items:
            items.remove(user_input)
            print(f"{user_input} removed from list, returning to main menu")
            return
            
        if reprompt(f"{user_input} is not in the list"):
            remove_item()
        print("Returning to main menu")
        return
        
    
def count_items() -> None:
    print("Counting")
    

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
