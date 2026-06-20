from menu_utils import MenuDict, show_menu, handle_menu_input
from string_utils import get_non_empty

def main() -> None:
    running = True

    def do_this() -> None:
        print("Doing this")
    

    def do_that() -> None:
        print("Doing that")


    def do_else() -> None:
        print("Doing something else")

    
    def exit_program() -> None:
        nonlocal running
        running = False


    menu: MenuDict = {
        "1": {
            'label' : "Do this",
            'command' : do_this
        },
        "2": {
            'label' : "Do that",
            'command' : do_that
        },
        "3": {
            'label' : "Do something else",
            'command' : do_else
        },
        "4": {
            'label' : "Exit program",
            'command' : exit_program
        }
    }

    while running:
        show_menu(menu)
        handle_menu_input(get_non_empty("Please select a menu option : "), menu)






if __name__ == "__main__":
    main()