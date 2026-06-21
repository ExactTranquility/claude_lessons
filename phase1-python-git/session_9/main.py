from classes.genshin_character import GenshinCharacter, TimedCharacter
from classes.genshin_weapon import GenshinWeapon
from classes.genshin_roster import CharacterRoster, WeaponRoster


if __name__ == "__main__":
    
    # print(oathkeeper.__dict__)
    # print(oathkeeper)
    # print(oathkeeper == bloody_smite)
    # oathkeeper.summary()
    
    diluc = GenshinCharacter("Diluc", level=10)
    s = GenshinCharacter("Hat Guy", level=10)
    hu_tao = TimedCharacter("Hu Tao", level=90, talent_lvl_basic=10, talent_lvl_skill=10)

    character_roster = CharacterRoster()

    character_roster.add(diluc)
    character_roster.add(hu_tao)
    character_roster.add(s)

    character_roster.list_all()

    character_roster.find('Hu Tao').update_levels("talent_lvl_burst", 10) # type : ignore

    character_roster.list_all()

    print(character_roster.return_maxed())


    oathkeeper = GenshinWeapon("Oathkeeper", 90, 90)
    bloody_smite = GenshinWeapon("Bloody Smite")

    weapon_roster = WeaponRoster()

    # weapon_roster.add(oathkeeper)
    # weapon_roster.add(bloody_smite)
    # print(weapon_roster.find('Oathkeeper').summary())
    weapon_roster.list_all()