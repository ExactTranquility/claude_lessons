from dataclasses import dataclass
from typing import ClassVar

@dataclass
class GenshinWeapon:
    name: str
    level: int = 1
    refine: int = 1

    MAX_LEVEL: ClassVar[int] = 90
    MAX_REFINE: ClassVar[int] = 5

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name cannot be blank")
        self.name = self.name.strip()
        self.level = max(1, min(self.level, self.MAX_LEVEL))
        self.refine = max(1, min(self.refine, self.MAX_REFINE))
        
    def __str__(self) -> str:
        return "{} is level {}\n{} is refined to rank {}".format(self.name, self.level, self.name, self.refine)
    
    # overwriting the default @dataclass to only comp level
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenshinWeapon):
            return NotImplemented
        return self.level == other.level
    
    def is_maxed(self) -> bool:
        return self.level == self.MAX_LEVEL and self.refine == self.MAX_REFINE
    
    def summary(self) -> str:
        return "\n{}\n{} is maxed out: {}".format(self ,self.name, self.is_maxed())