"""
This will be a cli persistant genshin character and weapon roster with stat tracking, this is single user only for now.
"""


# # TODO
# peristant json data read and write
# test first with a sample in app dataset

# main menu
# - character roster
#   - LATER IMPLIMENT MULIPLE ROSTERS
#   - view rosters
#   - reset roster
#       - are you sure(y/n)
#           - delete or return to previous menu
# - weapon roster
#   - LATER IMPLIMENT MULIPLE ROSTERS
#   - view rosters
#   - reset roster
#       - are you sure(y/n)
#           - delete or return to previous menu
# - exit_program

# List all character in your roster
# list maxed characters and unmaxed seperately?
# Get summary of a specific character
# Add a character
# delete a character
# exit back to main menu

# List all weapons in your roster : maxxed and unmaxed
# Get a summary of a specific weapon
# add a weapon
# delete a weapon
# exit back to main menu


from classes.genshin_character import GenshinCharacter, TimedCharacter
from classes.genshin_weapon import GenshinWeapon
from classes.genshin_roster import CharacterRoster, WeaponRoster
from utils.menu_utils import MainMenu, SubMenu

def placeholder_function() -> None:
    print("success")


def char_rost_open() -> None:
    char_menu_select = SubMenu.from_entries(
        ("View character roster", placeholder_function),
        ("Delete character roster", placeholder_function)
    )
    char_menu_select.run()


def weap_rost_open() -> None:
    weap_menu_select = SubMenu.from_entries(
        ("View character roster", placeholder_function),
        ("Delete character roster", placeholder_function)
    )
    weap_menu_select.run()


if __name__ == "__main__":
    
    menu = MainMenu.from_entries(
        ("Goto your character roster", char_rost_open),
        ("Do that", weap_rost_open),
    )
    
    menu.run()


    # diluc = GenshinCharacter("Diluc", level=10)
    # s = GenshinCharacter("Hat Guy", level=10)
    # hu_tao = TimedCharacter("Hu Tao", level=90, talent_lvl_basic=10, talent_lvl_skill=10)

    # character_roster = CharacterRoster()

    # character_roster.add(diluc)
    # character_roster.add(hu_tao)
    # character_roster.add(s)

    # character_roster.list_all()

    # character_roster.find('Hu Tao').update_levels("talent_lvl_burst", 10) # type : ignore

    # character_roster.list_all()

    # print(character_roster.return_maxed())


    # oathkeeper = GenshinWeapon("Oathkeeper", 90, 90)
    # bloody_smite = GenshinWeapon("Bloody Smite")

    # weapon_roster = WeaponRoster()

    # weapon_roster.add(oathkeeper)
    # weapon_roster.add(bloody_smite)
    # print(weapon_roster.find('Oathkeeper').summary())
    # weapon_roster.list_all()