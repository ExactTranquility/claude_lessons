from dataclasses import dataclass
from typing import ClassVar

@dataclass
class GenshinWeapon:
    name: str
    level: int = 1
    refine: int = 1

    FIELD_RANGES: ClassVar[dict[str, tuple[int, int]]] ={
        "level" : (1, 90),
        "refine" : (1, 5),
    }

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name cannot be blank")
        self.name = self.name.strip()

        for field_name, (low, high) in self.FIELD_RANGES.items():
            setattr(self, field_name, max(low, min(getattr(self, field_name), high)))
        
    def __str__(self) -> str:
        return "{} is level {}\n{} is refined to rank {}".format(self.name, self.level, self.name, self.refine)
    
    # overwriting the default @dataclass to only comp level
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenshinWeapon):
            return NotImplemented
        return self.level == other.level
    
    def _clamp(self, value: int, min_value: int, max_value: int) -> int:
        return max(min_value, min(value, max_value))

    def update_levels(self, field_name: str, value: int) -> None:
        if field_name not in self.FIELD_RANGES:
            raise ValueError(f"Unknown field: {field_name}")
        current = getattr(self, field_name)
        setattr(self, field_name, self._clamp(value + current, current, self.FIELD_RANGES[field_name][1]))


    def is_maxed(self) -> bool:
        return all(
            getattr(self, field_name) == high
            for field_name, (_, high) in self.FIELD_RANGES.items()
        )
    
    def summary(self) -> str:
        return "\n{}\n{} is maxed out: {}".format(self ,self.name, self.is_maxed())