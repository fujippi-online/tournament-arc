import random

from collections import defaultdict
from itertools import product

import message
import pronouns

from geometry import distance
from util import once
from meter import Meter
from settings import VIEW_WIDTH, VIEW_HEIGHT

class Character:
    blocks = True
    clear = True
    name = "Someone"
    is_hero = False
    pronouns = pronouns.neutral
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, scene):
        pass
    def ko_message(self):
        msg = "The {} collapses.".format(self.name)
        message.log.post(msg)
    def skill_check(self, skill, bar):
        result = self.roll_skill(skill)
        return result >= bar
    @property
    def position(self):
        return self.x, self.y
    def move_towards(self, scene, point, mask=[]):
        path = scene.path(self.position, point, mask = mask)
        step = path[0]
        if path and scene.passable(*step):
            self.x, self.y = step
    def move_away_from(self, scene, point):
        gaps = scene.background.adjacent(self.position) 
        gaps.append(self.position)
        steps = [p for p in gaps if scene.passable(*p)]
        step = max(steps, key = lambda p: distance(p, point))
        if step:
            self.x, self.y = step
    def hero_adjacent(self, scene):
        directions = product([-1, 0, 1], [-1, 0, 1]) 
        adjacent_spots = [(x+self.x, y+self.y) for x, y in directions]
        return scene.hero.position in adjacent_spots
    def random_step(self, scene):
        directions = product([-1, 0, 1], [-1, 0, 1]) 
        adjacent_spots = [(x+self.x, y+self.y) for x, y in directions]
        free_spots = [p for p in adjacent_spots if (not scene.things_at(*p) and
                not scene.background[p].blocks)]
        if free_spots:
            self.x, self.y = random.choice(free_spots)
    def action_hook(self, action_name, scene, **kwargs):
        hook_name = "on_"+action_name
        for stat in self.status:
            hook  = getattr(stat, hook_name, None)
            if hook:
                hook(self, scene, **kwargs)

class Follower(Character):
    color = "green"
    symbol = "F"
    name = "follower"
    def __init__(self, *args, **kwargs):
        Character.__init__(self, *args, **kwargs)
        self.move_speed = 0.6
        self.move_phase = 0
    def update(self, scene):
        Character.update(self, scene)
        self.move_phase += self.move_speed
        while self.move_phase > 1:
            self.move_towards(scene, scene.hero.position)
            self.move_phase -= 1 
    def interact(self, scene):
        message.log.post("Guy: HEY BUDDY LET'S BE FRIENDS")
    @once
    def seen(self):
        message.log.post("FUCK, IT'S THAT GUY. He's covered in blood.")


