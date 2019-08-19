import sys
from copy import copy

from .utils import sanitized_input, clear_screen
from .command_system import CommandSystem
from .character_system import CharacterSystem
from .treasure_system import TreasureSystem
from .player import Player
from .map import Map
from .saveload import SaveSystem
from .utils import parse_dice_format


class Game:
    def __init__(self):
        self.n_turns = 0
        self.screen_width = 80
        self.map = Map(self)
        self.player = Player(self)
        self.character_system = CharacterSystem(self)
        self.treasure_system = TreasureSystem(self)
        self.save_system = SaveSystem(self)
        self.command_system = CommandSystem(self)

    def next_turn(self):
        self.n_turns += 1
        command = sanitized_input("> ", error_msg="Invalid Command!")
        while not self.command_system.parse(command):
            print("Invalid command. Type 'help' for help.")
            command = sanitized_input("> ", error_msg="Invalid Command!")

    def main_menu(self):
        print("Welcome to rpg-text!")
        print("> New Game")
        print("> Load Game")
        print("> Quit")
        choice = sanitized_input("> ", error_msg="Invalid choice.").lower()
        if choice.startswith("n"):
            self.new_game()
        elif choice.startswith("l"):
            self.load_game()
        elif choice.startswith("q"):
            self.quit()

    def new_game(self):
        clear_screen()
        print("Please enter your character's name.")
        p_name = sanitized_input("> ", error_msg="")
        print("Please enter your desired job (thief, wizard, warrior, cleric).")
        p_job = sanitized_input("> ", error_msg="Invalid job.", valid_input=("thief", "wizard", "warrior", "cleric"))
        self.player.name = p_name
        self.player.job = p_job
        self.player.health_rolls.append(parse_dice_format(self.player.job.hp_die))
        self.player.mana_rolls.append(parse_dice_format(self.player.job.mp_die))

    def load_game(self):
        clear_screen()
        print("Enter a save name to load.")
        found_saves = SaveSystem.get_save_names()
        valid_inputs = copy(found_saves)
        valid_inputs.append("list")
        save_name = sanitized_input("> ", valid_input=valid_inputs, error_msg="Save file not found. Please try again.")
        if save_name.lower() == "list":
            print("Saves : " + ", ".join(found_saves))
        else:
            self.save_system.load(save_name)

    def quit(self):
        """Saves and quits the game. Save is named 'autosave'"""
        self.save_system.save("autosave")
        clear_screen()
        sys.exit(1)

    def serialize(self):
        return {"n_turns": self.n_turns}

    def deserialize(self, data):
        self.n_turns = data["n_turns"]
        return