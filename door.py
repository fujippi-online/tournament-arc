import random
import string

import message
import control
from inventory import Item
from util import once

class Door:
    name = "Door"
    def __init__(self, x, y):
        self.symbol = "+"
        self.x = x
        self.y = y
        self.encountered = False
        self.color = "yellow"
    @property
    def blocks(self):
        if self.symbol == "+":
            return True
        else:
            return False
    @property
    def clear(self):
        if self.symbol == "+":
            return False
        else:
            return True
    def seen(self):
        if not self.encountered:
            self.encountered = True
    def interact(self, scene):
        if self.symbol == "+":
            message.log.post("The door swings open.")
            self.symbol = "-"
        elif self.symbol == "-":
            message.log.post("You close the door.")
            self.symbol = "+"
    @property
    def position(self):
        return self.x, self.y

materials = ['silver',
        'iron',
        'copper',
        'bronze',
        'purple',
        'gold',
        'pewter',
        'brass',
        'stone',]

prefixes = [
        'common',
        'rusty',
        'ornate',
        'shiny',
        'sparkling',
        'glowing',
        'strange',
        'cold',
        'old',
        'big',
        'tiny',
        'spiral',
        'simple',
        'obtuse',
        'regal',
        'cheap',
        'fancy',
        'obtuse',
        'weird',
        'huge',
        'gothic',
        'triangular',
        'dull',
        'dirty',
        'angular',
        'rough',
        'polished',
        ]

def make_key_type():
    return random.choice(prefixes) + " " + random.choice(materials)

class Key(Item):
    symbol = "?"
    color = "magenta"
    blocks = True
    def __init__(self, key_type, position = (0,0)):
        self.key_type = key_type
        self.name = string.capwords(key_type) + " Key"
    def inspect(self, scene):
        message.log.post("A {} key.".format(self.key_type))

def make_key_type():
    return random.choice(prefixes) + " " + random.choice(materials)

class LockedDoor(Door):
    @property
    def name(self):
        return self.key_type.capitalize()+" Door"
    def __init__(self, x, y, key_type = "silver"):
        Door.__init__(self, x, y)
        self.key_type = key_type
    def interact(self, scene):
        inventory = scene.hero.inventory
        possible_keys = [item for item in inventory if (isinstance(item, Key) and
                item.key_type == self.key_type)]
        if possible_keys:
            message.log.post("You unlock the door's {} latch with a satisfying "
                    "click.".format(self.key_type))
            Door.interact(self, scene)
        else:
            message.log.post("The door is locked and you have no key to match "
                    "its {} lock.".format(self.key_type))
    @once
    def seen(self):
        message.log.post("You see a "+self.key_type+" door.")


