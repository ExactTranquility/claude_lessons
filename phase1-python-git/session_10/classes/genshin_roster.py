from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Roster(object):
    items_in_roster: list[object] = field(default_factory=list)

    LACK_OF_ENTRY_MSG: ClassVar[str] = "There are no entries yet!"
    def add(self, item: object) -> None:
        self.items_in_roster.append(item)

    def _find_index_by_name(self, name: str) -> int:
        """Private helper, return the index of the item if its in the roster, otherwise return -1 for None"""
        for idx, item in enumerate(self.items_in_roster):
            if getattr(item, 'name') == name:
                return idx
        return -1
    
    def remove(self, name: str) -> bool:
        idx = self._find_index_by_name(name)
        if idx != -1:
            self.items_in_roster.pop(idx)
            return True
        return False
        
    def find(self, name: str) -> object | None:
        idx = self._find_index_by_name(name)
        return self.items_in_roster[idx] if idx != -1 else None

    def summ_all(self) -> None:
        if not self.items_in_roster:
            print(self.LACK_OF_ENTRY_MSG)
            return
        for item in self.items_in_roster:
            print("{}\n".format(item.summary()))

    def return_maxed(self) -> str:
        if not self.items_in_roster:
            return self.LACK_OF_ENTRY_MSG
        
        maxed = "\n"
        for item in self.items_in_roster:
            if item.is_maxed():
                maxed += "{} is maxed out!\n".format(getattr(item, 'name'))
        return maxed if maxed.strip() else "No maxed entries."

@dataclass
class CharacterRoster(Roster):
    LACK_OF_ENTRY_MSG: ClassVar[str] = "There are no characters yet!"
    
    def list_all(self) -> None:
        maxed = []
        wip = []

        for item in self.items_in_roster:
            if item.is_maxed():
                maxed.append(getattr(item, 'name'))
        for item in self.items_in_roster:
            if not item.is_maxed():
                wip.append(getattr(item, 'name'))

        print("Maxed out characters\n------------------------")
        if not maxed:
            print("No maxxed out characters")
        else:
            for item in self.items_in_roster:
                if item.is_maxed():
                    print(getattr(item, 'name'))
            print()
        print("\nIn progress characters\n------------------------")
        if not wip:
            print("No in progress characters")
        else:
            for item in self.items_in_roster:
                if not item.is_maxed():
                    print(getattr(item, 'name'))
        print() 
        

@dataclass
class WeaponRoster(Roster):
    LACK_OF_ENTRY_MSG: ClassVar[str] = "There are no weapons yet!"

    def list_all(self) -> None:
        print("Maxed out characters\n------------------------")
        for item in self.items_in_roster:
            if item.is_maxed():
                print(getattr(item, 'name'))
        else:
            print("No maxxed out characters")
        print("\nIn progress characters\n------------------------")
        for item in self.items_in_roster:
            if not item.is_maxed():
                print(getattr(item, 'name'))
        else:
            print("No in progress characters")