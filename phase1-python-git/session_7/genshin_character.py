# If this was to be published again weapon and character would go in different classes,
# then assign the instance of the weapon to the character

class GenshinCharacter:
    MIN_CHARACTER_LVL = 1
    MAX_CHARACTER_LVL = 90

    MIN_TALENT_LVL = 1
    MAX_TALENT_LVL = 10

    MIN_CONSTELLATION = 0
    MAX_CONSTELLATION = 6

    MIN_WEAPON_LVL = 1
    MAX_WEAPON_LVL = 90

    MIN_WEAPON_REFINE = 1
    MAX_WEAPON_REFINE = 5

    def __init__(
        self,
        character_name: str,
        weapon_name: str,

        character_lvl: int = 1,
        talent_lvl_basic: int = 1,
        talent_lvl_skill: int = 1,
        talent_lvl_burst: int = 1,
        constellation: int = 0,
        
        weapon_lvl: int = 1,
        weapon_refine: int = 1

    ) -> None:
        if not character_name.strip():
            raise ValueError("Character name cannot be blank")
        if not weapon_name.strip():
            raise ValueError("Weapon name cannot be blank")
        
        self.character_name = character_name.strip()
        self.weapon_name = weapon_name.strip()

        self .character_lvl = self._clamp(character_lvl, self.MIN_CHARACTER_LVL, self.MAX_CHARACTER_LVL)
        self.talent_lvl_basic = self._clamp(talent_lvl_basic, self.MIN_TALENT_LVL, self.MAX_TALENT_LVL)
        self.talent_lvl_skill = self._clamp(talent_lvl_skill, self.MIN_TALENT_LVL, self.MAX_TALENT_LVL)
        self.talent_lvl_burst = self._clamp(talent_lvl_burst, self.MIN_TALENT_LVL, self.MAX_TALENT_LVL)
        self.constellation = self._clamp(constellation, self.MIN_CONSTELLATION, self.MAX_CONSTELLATION)

        self.weapon_lvl = self._clamp(weapon_lvl, self.MIN_WEAPON_LVL, self.MAX_WEAPON_LVL)
        self.weapon_refine = self._clamp(weapon_refine, self.MIN_WEAPON_REFINE, self.MAX_WEAPON_REFINE)

    
    def _clamp(self, value: int, min_value: int, max_value: int) -> int:
        return max(min_value, min(value, max_value))
    

    def _ismaxed(self) -> bool:
        return bool(
                self.character_lvl == self.MAX_CHARACTER_LVL
            and self.talent_lvl_basic == self.MAX_TALENT_LVL
            and self.talent_lvl_skill ==  self.MAX_TALENT_LVL
            and self.talent_lvl_burst == self.MAX_TALENT_LVL
            and self.constellation == self.MAX_CONSTELLATION
            and self.weapon_lvl == self.MAX_WEAPON_LVL
            and self.weapon_refine == self.MAX_WEAPON_REFINE
            )
    

    def _summary(self) -> None:
        stats = {
            "Character name" : self.character_name,
            "Character level" : self.character_lvl,
            "Talent levels": {
                "Basic" : self.talent_lvl_basic,
                "Skill" : self.talent_lvl_skill,
                "Burst" : self.talent_lvl_burst
            },
            "Constellation" : self.constellation,
            "Weapon name" : self.weapon_name,
            "Weapon level" : self.weapon_lvl,
            "Weapon refinement" : self.weapon_refine,
        }

        
        print()
        for i, value in stats.items():
            if type(value) == dict:
                count = 0
                print(f"{i} : ", end='')
                for _, value in value.items():
                    count += 1
                    if count != 1:
                        print("\t\t", end='')
                    print(f"{_} : {value}")
            else:
                print(f"{i} : {value}")

        print(f"{self.character_name} is maxed out : {self._ismaxed()}")
        print()


    def _upgrade(self, field: str, value: int) -> None:
        caps = {
            "character_lvl" : self.MAX_CHARACTER_LVL,
            "talent_lvl_basic" : self.MAX_TALENT_LVL,
            "talent_lvl_skill" : self.MAX_TALENT_LVL,
            "talent_lvl_burst" : self.MAX_TALENT_LVL,
            "constellation" : self.MAX_CONSTELLATION,
            "weapon_lvl" : self.MAX_WEAPON_LVL,
            "weapon_refine" : self.MAX_WEAPON_REFINE,
        }

        if field not in caps:
            raise ValueError(f"Unknown field: {field}")
        current = getattr(self, field)
        setattr(self, field, self._clamp(value + current, current, caps[field]))


if __name__ == "__main__":
    c = GenshinCharacter("Diluc", "Oathkeeper", character_lvl=80, weapon_lvl=80)
    c._summary()
    c._upgrade("talent_lvl_burst", 25)
    c._summary()