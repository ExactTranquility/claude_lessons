from typing import Callable, TypedDict
from collections.abc import Mapping

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


def clean_text(text: str) -> str:
    return " ".join(text.strip().split()).capitalize()


def add_item() ->  None:
    print("Adding")


def view_items() -> None:
    print("Viewing")
    
    
def remove_item() -> None:
    print("Removing")
    
    
def count_items() -> None:
    print("Counting")
    

def get_safe_input(prompt: str) -> str | None:
    while True:
        user_input = clean_text(input(prompt))
        if not user_input:
            return None
        return user_input


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
