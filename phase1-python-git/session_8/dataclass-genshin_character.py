from dataclasses import dataclass, field
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
    

    def summary(self) -> None:
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

        
        print()
        for label, stat_value in stats.items():
            if isinstance(stat_value, dict):
                count = 0
                print(f"{label} : ", end='')
                for sub_label, sub_value in stat_value.items():
                    count += 1
                    if count != 1:
                        print("\t\t", end='')
                    print(f"{sub_label} : {sub_value}")
            else:
                print(f"{label} : {stat_value}")

        print(f"{self.name} is maxed out : {self.is_maxed()}")
        print()


    def update_levels(self, field_name: str, value: int) -> None:
        if field_name not in self.FIELD_RANGES:
            raise ValueError(f"Unknown field: {field_name}")
        current = getattr(self, field_name)
        setattr(self, field_name, self._clamp(value + current, current, self.FIELD_RANGES[field_name][1]))


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


    # Not needed with @dataclass
    # def __repr__(self) -> str:
    #     return "GenshinWeapon(name={}, level={})".format(self.name, self.level)
    
    
    def __str__(self) -> str:
        return "{} is level {}\n{} is refined to rank {}".format(self.name, self.level, self.name, self.refine)
    
    # overwriting the default @dataclass to only comp level
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenshinWeapon):
            return NotImplemented
        return self.level == other.level
    
    def is_maxed(self) -> bool:
        return self.level == self.MAX_LEVEL and self.refine == self.MAX_REFINE
    
    def summary(self) -> None:
        print()
        print(self)
        print(f"{self.name} is maxed out: {self.is_maxed()}")





if __name__ == "__main__":
    c = GenshinCharacter("Diluc", level=90, talent_lvl_basic=10, talent_lvl_skill=10)
    print(c)
    c.summary()
    c.update_levels("talent_lvl_burst", 10)
    c.summary()

    oathkeeper = GenshinWeapon("Oathkeeper", 90, 90)
    bloody_smite = GenshinWeapon("Bloody Smite")
    print(oathkeeper.__dict__)
    print(oathkeeper)
    print(oathkeeper == bloody_smite)
    oathkeeper.summary()