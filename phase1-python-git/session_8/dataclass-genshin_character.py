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

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Character name cannot be blank")
        self.name = self.name.strip()

        for field, (low, high) in self.FIELD_RANGES.items():
            setattr(self, field, self._clamp(getattr(self, field), low, high))


    def __str__(self):
        str = ""
        for label, value in self.__dict__.items():
            str += "{} : {}\n".format(label, value)
        return str

    
    def _clamp(self, value: int, min_value: int, max_value: int) -> int:
        return max(min_value, min(value, max_value))
    

    def _ismaxed(self) -> bool:
        return all(
                getattr(self, field) == high
                for field, (_, high) in self.FIELD_RANGES.items()
                if field != 'constellation'
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

        print(f"{self.name} is maxed out : {self._ismaxed()}")
        print()


    def update_levels(self, field: str, value: int) -> None:
        if field not in self.FIELD_RANGES:
            raise ValueError(f"Unknown field: {field}")
        current = getattr(self, field)
        setattr(self, field, self._clamp(value + current, current, self.FIELD_RANGES[field][1]))


@dataclass
class GenshinWeapon:
    name: str
    level: int = 1
    refine: int = 1

    MAX_LEVEL: int = field(default=90, init=False, compare=False, repr=False)
    MAX_REFINE: int = field(default=5, repr=False, init=False, compare=False)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Name cannot be blank")
        setattr(self, self.name, self.name.strip())
        self.level = max(1, min(self.level, self.MAX_LEVEL))
        self.refine = max(1, min(self.refine, self.MAX_REFINE))


    # Not needed with @dataclass
    # def __repr__(self) -> str:
    #     return "GenshinWeapon(name={}, level={})".format(self.name, self.level)
    
    
    def __str__(self) -> str:
        return "{} is level {}\n{} is refined to rank {}".format(self.name, self.level, self.name, self.refine)
    
    # overwriting the default @dataclass to only comp level
    def __eq__(self, other) -> bool:
        return self.level == other
    
    def _ismaxed(self) -> bool:
        return self.level == self.MAX_LEVEL and self.refine == self.MAX_REFINE
    
    def summary(self) -> None:
        print()
        print(self)
        print(f"{self.name} is maxed out: {self._ismaxed()}")





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