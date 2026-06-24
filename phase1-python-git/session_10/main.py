"""
This will be a cli persistant genshin character and weapon roster with stat tracking, this is single user only for now.
"""


# # TODO
# peristant json data read and write
# test first with a sample in app dataset

# main menu
# - character roster !!!DONE!!!
#   - LATER IMPLIMENT MULIPLE ROSTERS
#   - view rosters !!!DONE!!! - singular
#   - reset roster !!!DONE!!!
#       - are you sure(y/n)
#           - delete or return to previous menu
# - weapon roster !!!DONE!!!
#   - LATER IMPLIMENT MULIPLE ROSTERS
#   - view rosters !!!DONE!!! -singular
#   - reset roster !!!DONE!!!
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


def character_roster_main() -> None:
    character_roster = CharacterRoster()

    character_roster.add(diluc)
    character_roster.add(hu_tao)
    character_roster.add(s)

    def find_handle() -> None:
        user_input = input("Name of the character you would like to see? : ").strip()
        print(character_roster.find(user_input))

    def add_character_handle() -> None:
        try:
            name = input("Name of character : ")
            level = int(input("Level : "))
            talent_lvl_basic = int(input("Basic attack level : "))
            talent_lvl_skill= int(input("Skill level : "))
            talent_lvl_burst= int(input("Burst level : "))
            constellation= int(input("Number of constellations : "))
        except ValueError:
            print("Invlaid arguements")

        c = GenshinCharacter(name, level, talent_lvl_basic, talent_lvl_skill, talent_lvl_burst, constellation)
        character_roster.add(c)


    character_main_menu = SubMenu.from_entries(
        ("List all characters you own", character_roster.list_all),
        ("Search for character", find_handle),
        ("Add a character", add_character_handle),
        ("Upgrade a character", placeholder_function),
        ("Delete a character", placeholder_function),
        )
    character_main_menu.run()

# Upgrade a character
# delete a character
# exit back to main menu


def weapon_roster_main() -> None:
    pass



def char_rost_open() -> None:
    char_menu_select = SubMenu.from_entries(
        ("View character roster", character_roster_main),
        ("Delete character roster", placeholder_function),
        term_on_transfer=True,
    )
    char_menu_select.run()


def weap_rost_open() -> None:
    weap_menu_select = SubMenu.from_entries(
        ("View weapon roster", placeholder_function),
        ("Delete weapon roster", placeholder_function),
        term_on_transfer=True,
    )
    weap_menu_select.run()


if __name__ == "__main__":
    
    menu = MainMenu.from_entries(
        ("Goto your character roster", char_rost_open),
        ("Goto your weapon roster", weap_rost_open),
    )
        
    diluc = GenshinCharacter("Diluc", level=10)
    s = GenshinCharacter("Hat Guy", level=10)
    hu_tao = TimedCharacter("Hu Tao", level=90, talent_lvl_basic=10, talent_lvl_skill=10)

    

    menu.run()
    

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