from dataclasses import dataclass, field



@dataclass
class Roster(object):
    items_in_roster: list[object] = field(default_factory=list)

    def add(self, item: object) -> None:
        self.items_in_roster.append(item)

    def _find_index_by_name(self, name: str) -> int:
        """Private helper, return the index of the item if its in the roster, otherwise return -1 for None"""
        for idx, item in enumerate(self.items_in_roster):
            if getattr(item, 'name') == name:
                return idx
        return -1
    
    def _is_roster_empty(self) -> bool:
        if not self.items_in_roster:
            print("There are no characters yet!")
            return True
        return False

    def remove(self, name: str) -> bool:
        idx = self._find_index_by_name(name)
        if idx != -1:
            self.items_in_roster.pop(idx)
            return True
        return False
        
    def find(self, name: str) -> object | None:
        idx = self._find_index_by_name(name)
        return self.items_in_roster[idx] if idx != -1 else None

    def list_all(self) -> None:
        if self._is_roster_empty():
            return
        for item in self.items_in_roster:
            print(item.summary())

    def return_maxed(self) -> str:
        if self._is_roster_empty():
            return ""
        
        maxed = "\n"
        for item in self.items_in_roster:
            if item.is_maxed():
                maxed += "{} is maxed out!\n".format(getattr(item, 'name'))
        return maxed

@dataclass
class CharacterRoster(Roster):
    pass

@dataclass
class WeaponRoster(Roster):
    pass