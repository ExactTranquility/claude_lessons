from dataclasses import dataclass, field
from typing import TypedDict, Callable, Self

class MenuEntry(TypedDict):
    label: str
    command: Callable[[], None]

@dataclass
class Menu:
    running: bool = False
    term_on_transfer: bool = False

    menu: list[MenuEntry] = field(default_factory=list)

    @classmethod
    def from_entries(cls, *entries, term_on_transfer: bool=False) -> Self:
        menu_entries = []
        for label, command in entries:
            menu_entries.append({'label' : label, 'command': command})
        return cls(term_on_transfer=term_on_transfer, menu=menu_entries)
        

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

    def handle_idx_input(self, user_input) -> bool:
        if not user_input:
            print("Entry cannot be empty, please try again.")
            return False
        user_input = self._safe_int(user_input)
        if user_input is None:
            print("Not a valid choice, please enter the number of the menu option you want to select.")
            return False
        if not 1 <= user_input <= len(self.menu):
            print(f"Invalid menu option, please choose a number between 1 and {len(self.menu)}")
            return False
        
        for idx, menu_item in enumerate(self.menu):
            if  user_input - 1 == idx:
                menu_item["command"]()
                return True
        return False

    def exit_menu(self) -> None:
        print("Exiting now.")
        self.running = False

    def handle_transfer(self, user_input) -> None:
        if self.handle_idx_input(user_input):
            if self.term_on_transfer:
                self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            self.show_menu()
            self.handle_transfer(self.get_menu_input())

@dataclass
class MainMenu(Menu):

    def __post_init__(self):
        self.menu.append({'label' : "Exit program", 'command' : self.exit_menu})


@dataclass
class SubMenu(Menu):
    

    def __post_init__(self):
        menu_string = "previous menu" if self.term_on_transfer else "main menu"
        self.menu.append({'label' : "Return to the {}".format(menu_string), 'command' : self.exit_menu})

    def exit_menu(self) -> None:
        print("Returning to previous menu.\n")
        self.running = False