import json
from .utils import parse_dice_format
from .player import Player


class Item:
    def __init__(self, name):
        self.name = name
        with open("data/items.json") as f:
            data = json.load(f).get("name", {})

        self.equippable = data.get("equippable", False)
        self.useable = data.get("useable", False)
        self.weapon_type = data.get("weapon_type", "melee")
        self.effects_on_hit = data.get("effects_on_hit", [])
        self.damage_die = data.get("damage", "1d6")
        self.damage_modifier = data.get("damage_modifier", 0)
        self.hit_modifier = data.get("hit_modifier", 0)
        self.slot = data.get("slot", "")
        self.price = data.get("price", 0)
        self._display_name = data.get("display_name", None)
        self.effects_on_equip = data.get("effects_on_equip", [])
        self.description = data.get("description", "")
        self.effects_on_use = data.get("effects_on_use", [])

    @property
    def display_name(self):
        if self._display_name is None:
            return self.name.replace("_", " ").capitalize()
        else:
            return self.display_name

    @property
    def damage(self):
        return parse_dice_format(self.damage_die) + self.damage_modifier

    def use(self, target):
        if self.useable:
            target.inflict_status_effects(*self.effects_on_use)
            if isinstance(target, Player):
                pronoun = 'you'
            else:
                pronoun = target.name
            print(f"You used {self.display_name} which granted {pronoun} {', '.join(self.effects_on_use)}!")
        else:
            print("You can't use this item!")
        pass
