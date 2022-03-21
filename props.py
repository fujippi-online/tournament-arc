import message
import menu
import control
import core
import random

class Smoke:
    name = "Smoke"
    color = "black"
    symbol = chr(167)
    blocks = False
    clear = False
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time
    @property
    def position(self):
        return self.x, self.y
    def update(self, scene):
        self.time -= 1
        if self.time == 0:
            scene.destroy(self)

class Fog:
    name = "Fog"
    color = "bright_black"
    symbol = chr(167)
    blocks = False
    clear = False
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time
    @property
    def position(self):
        return self.x, self.y
    def update(self, scene):
        if random.random() < 0.05:
            self.x -= 1
        elif random.random() < 0.3:
            self.y += random.choice([-1, 1])
        self.time -= 1
        if self.time == 0:
            scene.destroy(self)
class Mist(Fog):
    name = "Mist"
    color = "white"
    blocks = False
    clear = True

class Sign:
    name = "Sign"
    color = "black"
    bg_color = "yellow"
    symbol = "="
    blocks = True
    clear = False
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.have_seen = False
        self.text = text
    @property
    def position(self):
        return self.x, self.y
    def seen(self):
        if not self.have_seen:
            self.have_seen = True
            message.log.post("You see a sign that says \"{}\"".format(self.text))
    def interact(self, scene):
        message.log.post("Sign: "+self.text)


class Barrel:
    name = "Barrel"
    color = "black"
    bg_color = "yellow"
    symbol = "B"
    blocks = True
    clear = False
    def __init__(self, x, y, contents):
        self.x = x
        self.y = y
        self.have_seen = False
        self.contents = contents
    @property
    def position(self):
        return self.x, self.y
    def interact(self, scene):
        if self.contents != []:
            contents_options = [(thing.name, thing) for thing in self.contents]+\
                    [("Done","Done")]
            chosen_item = None
            contents_menu = menu.FloatingMenu(scene, 0, 0, contents_options,
                    title = "{} Contents".format(self.name))
            while True:
                chosen_item = control.takeover(contents_menu)
                if chosen_item == "Done" or len(contents_options) == 1:
                    break
                else:
                    contents_menu.remove((chosen_item.name, chosen_item))
                    self.contents.remove(chosen_item)
                    scene.hero.inventory.append(chosen_item)
                    message.log.post("You take the {}.".format(chosen_item.name))
        else:
            message.log.post("The {} is empty.".format(self.name))
            
class Crate(Barrel):
    name = "Crate"
    symbol = "#"

class Chest(Barrel):
    name = "Treasure Chest"
    symbol = "+"

