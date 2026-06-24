from dataclasses import dataclass, field
from datetime import date
from typing import ClassVar

@dataclass
class GenshinCharacter:
    name: str = field(compare=False)
    level: int = 1
    talent_lvl_basic: int = 1
    talent_lvl_skill: int = 1
    talent_lvl_burst: int = 1
    constellation: int = field(default=0, compare=False)

    FIELD_RANGES: ClassVar[dict[str, tuple[int, int]]] = {
        "level"             : (1, 90),
        "talent_lvl_basic"  : (1, 10),
        "talent_lvl_skill"  : (1, 10),
        "talent_lvl_burst"  : (1, 10),
        "constellation"     : (0, 6),
    }

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Character name cannot be blank")
        self.name = self.name.strip()

        for field_name, (low, high) in self.FIELD_RANGES.items():
            setattr(self, field_name, self._clamp(getattr(self, field_name), low, high))


    def __str__(self) -> str:
        display_text = ""
        for label, value in self.__dict__.items():
            display_text += "{} : {}\n".format(label, value)
        return display_text
    
    def _clamp(self, value: int, min_value: int, max_value: int) -> int:
        return max(min_value, min(value, max_value))

    def is_maxed(self) -> bool:
        return all(
                getattr(self, field_name) == high
                for field_name, (_, high) in self.FIELD_RANGES.items()
                if field_name != 'constellation'
        )

    def summary(self) -> str:
        stats = {
            "Character name" : self.name,
            "Character level" : self.level,
            "Talent levels": {
                "Basic" : self.talent_lvl_basic,
                "Skill" : self.talent_lvl_skill,
                "Burst" : self.talent_lvl_burst
            },
            "Constellation" : self.constellation,
        }
        
        # Return a format string instead of print.
        summ = ""
        for label, stat_value in stats.items():
            if isinstance(stat_value, dict):
                summ += f"{label} : "
                for idx , (sub_label, sub_value) in enumerate(stat_value.items(), 0):
                    if idx != 0:
                        summ += "\t\t"
                    summ += f"{sub_label} : {sub_value}\n"
            else:
                summ += f"{label} : {stat_value}\n"
        summ += f"{self.name} is maxed out : {self.is_maxed()}"

        return summ

    def update_levels(self, field_name: str, value: int) -> None:
        if field_name not in self.FIELD_RANGES:
            raise ValueError(f"Unknown field: {field_name}")
        current = getattr(self, field_name)
        setattr(self, field_name, self._clamp(value + current, current, self.FIELD_RANGES[field_name][1]))


@dataclass
class TimedCharacter(GenshinCharacter):
    date_added: date = field(default_factory=date.today)

    def summary(self) -> str:
        base = super().summary()
        return f"{base}\nDate pulled : {self.date_added}"