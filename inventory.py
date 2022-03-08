import string
import itertools
import collections

import settings
import control
import message

from util import once
from core import term

class Item:
    name = "Null Item"
    symbol = "0"
    color = "yellow"
    clear = True
    blocks = False
    def __init__(self, position = (0,0)):
        self.x, self.y = position
        self.been_seen = False
    def use(self, scene):
        return control.DONE
    @property
    def position(self):
        return self.x, self.y
    def inspect(self, scene):
        message.log.post("It's nothing.")
        return control.DONE
    def drop(self, scene):
        scene.hero.inventory.remove(self)
        self.x, self.y = scene.hero.position
        scene.foreground.append(self)
        message.log.post("Dropped "+self.name)
    def interact(self, scene):
        self.pick_up(scene)
    def pick_up(self, scene):
        inventory = scene.hero.inventory
        inventory.append(self)
        scene.foreground.remove(self)
        letter = string.ascii_letters[len(inventory)-1]
        message.log.post(letter+" - "+self.name)
    def seen(self):
        if not self.been_seen:
            message.log.post("There's a "+self.name+".")
            self.been_seen = True
    def __repr__(self):
        return self.name

class Inventory:
    def __init__(self, scene):
        self.scene = scene
        items = scene.hero.inventory
        num_items = len(scene.hero.inventory)
        self.options = collections.OrderedDict(
                list(zip(string.ascii_letters[:num_items], items)))
        self.modes = itertools.cycle(["drop", "inspect", "use"])
        self.mode = 'use'
        self.position = 0
    def update_use(self, key):
        return self.options[key].use(self.scene)
    def update_inspect(self, key):
        self.options[key].inspect(self.scene)
    def update_drop(self, key):
        self.options[key].drop(self.scene)
        return control.DONE
    def cycle_mode(self):
        self.mode = next(self.modes) 
    def update(self, key):
        if key in self.options:
            mode_update = getattr(self, "update_"+self.mode)
            return mode_update(key)
        elif key == ' ':
            self.cycle_mode()
        elif key.name == "KEY_ESC":
            return control.DONE
    def render(self):
        first = self.position
        last = min(first + settings.VIEW_HEIGHT-2, len(list(self.options.items())))
        visible_options = list(self.options.items())[first:last]
        with term.location(0,0):
            for index, item in visible_options:
                print((index+" - "+item.name))
        with term.location(0, settings.VIEW_HEIGHT-1):
            print(("MODE:"+self.mode+" SPACE: change mode"))

