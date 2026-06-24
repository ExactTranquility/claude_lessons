"""
This will be a cli persistant genshin character and weapon roster with stat tracking, this is single user only for now.
"""


# # TODO
# peristant json data read and write
# test first with a sample in app dataset

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

    def upgrade_handle() -> None:
        user_input = input("Name of the character you would like to upgrade? : ").strip()
        char: GenshinCharacter = character_roster.find(user_input)
        print(char.FIELD_RANGES)
        field = input("What field do you want to update? : ").strip()
        value = int(input("What level do you want to assign? (Must be a number) : "))
        char.update_levels(field, value)
        
    def delete_handle() -> None:
        user_input = input("Name of the character you would like to delete? : ").strip()
        character_roster.remove(user_input)
        print("Character deleted successfully")

    character_main_menu = SubMenu.from_entries(
        ("List all characters you own", character_roster.list_all),
        ("Search for character", find_handle),
        ("Add a character", add_character_handle),
        ("Upgrade a character", upgrade_handle),
        ("Delete a character", delete_handle),
        )
    character_main_menu.run()


def weapon_roster_main() -> None:
    pass



def char_rost_open() -> None:
    char_menu_select = SubMenu.from_entries(
        ("View character roster", character_roster_main),
        # ("Delete character roster", placeholder_function),
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
        # ("Goto your weapon roster", weap_rost_open),
    )
    menu.run()
    

    # oathkeeper = GenshinWeapon("Oathkeeper", 90, 90)
    # bloody_smite = GenshinWeapon("Bloody Smite")
    # weapon_roster = WeaponRoster()
    # weapon_roster.add(oathkeeper)
    # weapon_roster.add(bloody_smite)
    # print(weapon_roster.find('Oathkeeper').summary())
    # weapon_roster.list_all()