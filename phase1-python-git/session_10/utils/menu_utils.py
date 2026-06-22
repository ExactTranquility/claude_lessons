from dataclasses import dataclass, field
from typing import TypedDict, Callable

def do_this() -> None:
    print("Doing this")

def do_that() -> None:
    print("Doing that")

def do_something() -> None:
    print("Doing something else")



class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

@dataclass
class Menu:
    running: bool = False

    menu: list[MenuEntry] = field(default_factory=list)

    def add_menu_entry(self, label: str, command: Callable[[], None]) -> None:
        entry: MenuEntry = {"label" : label, "command" : command}
        self.menu.append(entry)

    def show_menu(self) -> None:
        for idx, menu_item in enumerate(self.menu, 1):
            print(f"{idx}.) {menu_item['label']}")
        print()

    def get_menu_input(self) -> str:
        return input("Please select a menu option : ").strip()
    
    def _safe_int(self, text: str) -> int | None:
        try:
            return int(text)
        except ValueError:
            return None

    def handle_idx_input(self, user_input) -> None:
        if not user_input:
            print("Entry cannot be empty, please try again.")
            return
        user_input = self._safe_int(user_input)
        if user_input is None:
            print("Not a valid choice, please enter the number of the menu option you want to select.")
            return
        
        for idx, menu_item in enumerate(self.menu):
            if  user_input - 1 == idx:
                menu_item["command"]()

    def exit_menu(self) -> None:
        print("Exiting now.")
        self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            self.show_menu()
            self.handle_idx_input(self.get_menu_input())


menu = Menu()
menu.add_menu_entry("Do this", do_this)
menu.add_menu_entry("Do that", do_that)
menu.add_menu_entry("Do something else", do_something)
menu.add_menu_entry("Exit program", menu.exit_menu)


menu.run()