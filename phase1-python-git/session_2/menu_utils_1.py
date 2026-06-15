
from typing import Callable, TypedDict
from collections.abc import Mapping



class MenuEntry(TypedDict):
    label : str
    command: Callable[[], None]

MenuDict = Mapping[str, MenuEntry]


def show_menu(menu: MenuDict) -> None:    
    print()
    for index, menu_entry in menu.items():
        print(f"{index}.) {menu_entry['label']}")
    print()


def get_clean_text(prompt: str) -> str:
    while True:
        user_input = " ".join(input(prompt).strip().split()).lower()
        
        if not user_input:
            print("Input cannot be blank, please try again")
            continue
        return user_input        
        
        
def handle_menu_input(user_input:str, menu: MenuDict) -> None:
    choice = menu.get(user_input)
    if choice is None:
        print("Invalid option, please try again")
    else:
        choice['command']()
    

def do_this() -> None:
    print("Doing this")
    
    
def do_that() -> None:
    print("Doing that")


def main() -> None:
    running = True
    
    def exit_program() -> None:
        nonlocal running
        running = False
    
    menu : MenuDict = {
        "1" : {
            "label" : "Do this",
            "command" : do_this
        },
        "2" : {
            "label" : "Do that",
            "command" : do_that
        },
        "3" : {
            "label" : "Exit program",
            "command" : exit_program
        }
    }
    
    while running:
        show_menu(menu)
        handle_menu_input(get_clean_text("Choose a menu option: "), menu)
    

if __name__ == "__main__":
    main()