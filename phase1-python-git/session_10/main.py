"""
This will be a cli persistant genshin character and weapon roster with stat tracking, this is single user only for now.
"""

# # TODO
# List all weapons in your roster : maxxed and unmaxed
# Get a summary of a specific weapon
# add a weapon
# delete a weapon
# exit back to main menu


from classes.genshin_character import GenshinCharacter, TimedCharacter
from classes.genshin_weapon import GenshinWeapon
from classes.genshin_roster import CharacterRoster, WeaponRoster
from dataclasses import asdict
from pathlib import Path
from utils.menu_utils import MainMenu, SubMenu
import json

absolute_path = Path(__file__).parent

def json_load(path: Path) -> list:
    try:
        with open(path, 'r') as c:
            return json.load(c)
    except FileNotFoundError:
        print("!!!WARNING!!! File does not exist, starting with empty list.")
        return []
    except json.JSONDecodeError:
        print("!!!WARNING!!! Data cannot be read, starting with empty list")
        return []


def json_save(file: object, path: Path) -> None:
    serialized = [asdict(item) for item in file]
    with open(path, 'w') as f:
        json.dump(serialized, f, indent=2)
                

def placeholder_function() -> None:
    print("success")


def character_roster_main() -> None:
    character_path: Path = absolute_path / 'characters.json'
    char_roster = json_load(character_path)
    character_roster = CharacterRoster()
    for char in char_roster:
        character_roster.add(GenshinCharacter(**char))

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
            print()
        except ValueError:
            print("Invalid arguements")
            return

        c = GenshinCharacter(name, level, talent_lvl_basic, talent_lvl_skill, talent_lvl_burst, constellation)
        character_roster.add(c)
        json_save(character_roster.items_in_roster, character_path)

    def upgrade_handle() -> None:
        user_input = input("Name of the character you would like to upgrade? : ").strip()
        char: GenshinCharacter = character_roster.find(user_input)
        if char is None:
            print("Character does not exist")
            return
        print(char.FIELD_RANGES)
        field = input("What field do you want to add to? : ").strip()
        try:
            value = int(input("How much do you want to add? (Must be a number) : "))
        except ValueError:
            print("That was not a number, returning to menu")
            return
        char.update_levels(field, value)
        json_save(character_roster.items_in_roster, character_path)
        print()
        
    def delete_handle() -> None:
        user_input = input("Name of the character you would like to delete? : ").strip()
        if character_roster.remove(user_input):
            print("Character deleted successfully\n")
            json_save(character_roster.items_in_roster, character_path)
        else:
            print("Character not deleted(Possibly mispelled?)\n")

    character_main_menu = SubMenu.from_entries(
        ("List all characters you own", character_roster.list_all),
        ("Search for character", find_handle),
        ("Add a character", add_character_handle),
        ("Upgrade a character", upgrade_handle),
        ("Delete a character", delete_handle),
        )
    character_main_menu.run()


def weapon_roster_main() -> None:
    weapon_path: Path = absolute_path / 'weapons.json'
    weap_roster = json_load(weapon_path)
    weapon_roster = WeaponRoster()
    for weap in weap_roster:
        weapon_roster.add(GenshinWeapon(**weap))

    def find_handle() -> None:
        user_input = input("Name of the weapon you would like to see? : ").strip()
        print(weapon_roster.find(user_input))

    def add_weapon_handle() -> None:
        try:
            name = input("Name of weapon : ")
            level = int(input("Level : "))
            refine = int(input("Number of Refinements : "))
            print()
        except ValueError:
            print("Invalid arguements")
            return

        w = GenshinWeapon(name, level, refine)
        weapon_roster.add(w)
        json_save(weapon_roster.items_in_roster, weapon_path)

    def upgrade_handle() -> None:
        user_input = input("Name of the weapon you would like to upgrade? : ").strip()
        weap: GenshinWeapon = weapon_roster.find(user_input)
        if weap is None:
            print("Weapon does not exist")
            return
        print(weap.FIELD_RANGES)
        field = input("What field do you want add to? : ").strip()
        try:
            value = int(input("How much do you want to add? (Must be a number) : "))
        except ValueError:
            print("That was not a number, returning to menu")
            return
        weap.update_levels(field, value)
        json_save(weapon_roster.items_in_roster, weapon_path)
        print()
        
    def delete_handle() -> None:
        user_input = input("Name of the weapon you would like to delete? : ").strip()
        if weapon_roster.remove(user_input):
            print("Weapon deleted successfully\n")
            json_save(weapon_roster.items_in_roster, weapon_path)
        else:
            print("Weapon not deleted(Possibly mispelled?)\n")

    weapon_main_menu = SubMenu.from_entries(
        ("List all weapons you own", weapon_roster.list_all),
        ("Search for weapon", find_handle),
        ("Add a weapon", add_weapon_handle),
        ("Upgrade a weapon", upgrade_handle),
        ("Delete a weapon", delete_handle),
        )
    weapon_main_menu.run()



def char_rost_open() -> None:
    char_menu_select = SubMenu.from_entries(
        ("View character roster", character_roster_main),
        # ("Delete character roster", placeholder_function),
        term_on_transfer=True,
    )
    char_menu_select.run()


def weap_rost_open() -> None:
    weap_menu_select = SubMenu.from_entries(
        ("View weapon roster", weapon_roster_main),
        # ("Delete weapon roster", placeholder_function),
        term_on_transfer=True,
    )
    weap_menu_select.run()


if __name__ == "__main__":
    
    menu = MainMenu.from_entries(
        ("Goto your character roster", char_rost_open),
        ("Goto your weapon roster", weap_rost_open),
    )
    menu.run()
    

    # oathkeeper = GenshinWeapon("Oathkeeper", 90, 90)
    # bloody_smite = GenshinWeapon("Bloody Smite")
    # weapon_roster = WeaponRoster()
    # weapon_roster.add(oathkeeper)
    # weapon_roster.add(bloody_smite)
    # print(weapon_roster.find('Oathkeeper').summary())
    # weapon_roster.list_all()