

def add_item() ->  None:
    pass


def view_items() -> None:
    pass
    
    
def remove_item() -> None:
    pass
    
    
def count_items() -> None:
    pass
    
    
def quit() -> None:
    pass
    

def get_safe_input(prompt: str) -> str:
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input
        print("Invalid input, please try again")


# menu item, callable
menu = {
    "1" : {"label" : "Add item", "command" : add_item},
    "2" : {"label" : "View items", "command" : view_items},
    "3" : {"label" : "Remove item", "command" : remove_item},
    "4" : {"label" : "Count items", "command" : count_items},
    "5" : {"label" : "Quit", "command" : quit}
}


# : dict[index: int, callable()]
def show_menu(menu) -> None:
    for key, entry in menu.items():
        print(f"{key}.) {entry['label']}")
        



def main() -> None:
    show_menu(menu)


if __name__ == "__main__":
    main()
