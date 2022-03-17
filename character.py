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
    body_parts = True
    pronouns = pronouns.neutral
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, scene):
        pass
    @property
    def position(self):
        return self.x, self.y
    def move_towards(self, scene, point, mask=[]):
        path = scene.path(self.position, point, mask = mask)
        if not path:
            return
        step = path[0]
        if scene.passable(*step):
            self.x, self.y = step
            scene.recache_position(self)
    def move_away_from(self, scene, point):
        gaps = scene.background.adjacent(self.position) 
        gaps.append(self.position)
        steps = [p for p in gaps if scene.passable(*p)]
        step = max(steps, key = lambda p: distance(p, point))
        if step:
            self.x, self.y = step
            scene.recache_position(self)
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

class Follower(Character):
    color = "green"
    symbol = "F"
    name = "follower"
    def __init__(self, x, y):
        Character.__init__(self, x, y)
        self.move_speed = 0.6
        self.move_phase = 0
    def update(self, scene):
        Character.update(self, scene)
        self.move_phase += self.move_speed
        while self.move_phase > 1:
            self.move_towards(scene, scene.hero.position)
            self.move_phase -= 1 
    def interact(self, scene):
        message.log.post("Guy: ")
    @once
    def seen(self):
        message.log.post("Uh oh.")


