import sys

import blessed

import roguemap
import message
import map_generators
import geometry
import menu
import inspect_scene
import game_time

from settings import VIEW_WIDTH, VIEW_HEIGHT
from core import DIRECTIONS, term
from camera import Camera
from character import Character
from pathing import path, Mask
from control import takeover, TargetPicker

class Hero(Character):
    name = "You"
    symbol = "@"
    color = "blue_on_white"
    inventory = []
    is_hero = True
    vision_range = 8
    def say(self, spoken_message):
        message.log.post(self.name+": "+spoken_message)


DEFAULT_AMBIANCE = ["Things are going well."
        ]
class MapScene:
    def __init__(self, ambiance = DEFAULT_AMBIANCE):
        self.background = roguemap.Map()
        self.foreground = []
        self.undercoat = []
        self.hero = Hero(5,5)
        self.camera = Camera(0, 0, VIEW_WIDTH, VIEW_HEIGHT)
        self.camera.center_on(self.hero)
        self.seen = set()
        self.turn_num = 0
        self.to_remove = []
        self.ambiance = ambiance
        self.transition_with = None
        self.location_cache = {}
        self.locations_cached = False
    def show_message(self, lines):
        msgbox = menu.MessageBox(lines, bg = self)
        takeover(msgbox, clear = False)
    def blocks_sight(self, x, y):
        for thing in self.things_at(x,y):
            if not thing.clear:
                return True
        return self.background[(x,y)].clear == False
    def build_location_cache(self):
        for thing in self.foreground:
            try:
                self.location_cache[thing.position].append(thing)
            except KeyError:
                self.location_cache[thing.position] = [thing]
        self.locations_cached = True
    def reset_location_cache(self):
        self.location_cache = {}
        self.locations_cached = False
    def things_at(self, x, y):
        if not self.locations_cached:
            self.build_location_cache()
        try:
            return list(self.location_cache[(x,y)])
        except KeyError:
            return []
    def passable(self, x, y):
        if self.background[(x,y)].blocks == True:
            return False
        for thing in self.things_at(x, y):
            if thing.blocks:
                return False
        return True
    def path(self, p1, p2, mask = []):
        block_mask = [Mask(x, y) for (x,y) in mask]
        p = path(self.background, p1, p2, things = self.foreground + [self.hero]
                + block_mask)
        return p
    def visible(self, p1, p2, vision_range = None):
        """
        Check if p2 is visible from p1 and vice versa using line algorithm.
        """
        x2, y2 = p2
        for x, y in geometry.iter_line(p1, p2):
            if self.blocks_sight(x,y) and ((x != x2) or (y != y2)):
                return False
            if vision_range and geometry.distance(p1, (x,y)) > vision_range:
                return False
        return True
    def interact_local(self):
        picker = TargetPicker(self, box = (1,1))
        spot = takeover(picker)
        for thing in self.things_at(*spot):
            if hasattr(thing, 'interact'):
                thing.interact(self)
                break
    def inspect_scene(self):
        inspector = inspect_scene.Inspector(self)
        takeover(inspector)
    def do_command(self, signal):
        hero = self.hero
        if signal.name and signal.name in DIRECTIONS:
            dx, dy = DIRECTIONS[signal.name]
            new_tile = hero.x + dx, hero.y + dy
            if self.passable(*new_tile):
                hero.x += dx
                hero.y += dy
            else:
                for thing in self.things_at(*new_tile):
                    if hasattr(thing, 'interact'):
                        thing.interact(self)
        elif hasattr(self, signal.name):
            getattr(self, signal.name)()
    def quit(self):
        quit_menu = menu.FloatingMenu(2, 1, [
            ("Resume", lambda: None),
            ("Items", lambda: self.inventory()),
            ("Quit", lambda: sys.exit()),
            ], title = "Quit?", bg = self)
        takeover(quit_menu)
    def inventory(self):
        chosen_action = "Cancel" 
        inventory_items = [(item.name, item) for item in self.hero.inventory]
        class Quit:
            name = "Quit"
            description = "Quit the inventory menu."
            symbol = "Q"
            color = "red"
        inventory_items.append(("Quit", Quit()))
        inventory_menu = menu.InfoPanelMenu(inventory_items,
                title = "Inventory", info_fields = ["name", "symbol"])
        possible_actions = [
                ("Use", "Use"),
                ("Drop", "Drop"),
                ("Cancel", "Cancel"),
        ]
        while chosen_action == "Cancel":
            chosen_item = takeover(inventory_menu)
            if chosen_item.__class__ == Quit:
                return
            chosen_action = takeover(inventory_menu.submenu(possible_actions))
        if chosen_action == "Drop":
            chosen_item.drop(self)
        if chosen_action == "Use":
            chosen_item.use(self)
    def update(self, signal):
        self.reset_location_cache()
        self.turn_num += 1
        self.do_command(signal)
        for thing in self.foreground:
            if hasattr(thing, 'update'):
                thing.update(self)
        self.hero.update(self)
        for u in self.undercoat:
            u.update(self)
        self.camera.center_on(self.hero)
        for thing in self.to_remove:
            if thing in self.foreground:
                self.foreground.remove(thing)
        self.to_remove = []
        game_time.calendar.update()
    def destroy(self, other):
        self.to_remove.append(other)
    def render(self):
        camera = self.camera
        object_positions = set()
        hero = self.hero
        with term.location(*camera.adjust(hero.x, hero.y)):
            color = getattr(term, hero.color)
            print((color(hero.symbol)))
            object_positions.add(hero.position)
        for thing in self.foreground:
            if geometry.point_in_rect(camera.rect, thing.position):
                sx, sy = camera.adjust(*thing.position)
                if self.visible(hero.position, thing.position, 
                        vision_range = hero.vision_range)\
                        and hero.position != thing.position:
                    object_positions.add(thing.position)
                    if hasattr(thing, 'hero_seen'):
                        thing.hero_seen = hero.position
                    with term.location(sx, sy):
                        if hasattr(thing, "bg_color"):
                            color = getattr(term, thing.color+"_on_"+thing.bg_color)
                        else:
                            color = getattr(term, thing.color+"_on_bright_black")
                        if hasattr(thing, 'body_parts'):
                            print((color(term.on_white(thing.symbol))))
                        else:
                            print((color(thing.symbol)))
                    if hasattr(thing, 'seen'):
                        thing.seen()
                    thing.last_seen = thing.position
                elif (hasattr(thing, 'last_seen')
                        and geometry.point_in_rect(camera.rect,
                                thing.last_seen)
                        and thing.last_seen not in object_positions
                        and (not self.visible(hero.position,
                            thing.last_seen))):
                    sx, sy = camera.adjust(*thing.last_seen)
                    with term.location(sx, sy):
                        print((term.bright_black_on_black(thing.symbol)))
                    object_positions.add(thing.last_seen)
        visible_tiles = self.background.submap(*camera.rect)
        x = 0
        for col in visible_tiles:
            y = 0
            for tile in col:
                wx, wy = camera.invert(x,y)
                if (wx, wy) not in object_positions:
                    if self.visible(hero.position, (wx,wy), vision_range =
                            hero.vision_range):
                        with term.location(x,y):
                            self.seen.add((wx, wy))
                            t_color = getattr(term, tile.color)
                            print((term.on_bright_black(t_color(tile.symbol))))
                    else:
                        with term.location(x,y):
                            if (wx, wy) in self.seen:
                                print((term.bright_black_on_black(tile.symbol)))
                            else:
                                print((term.on_black(' ')))
                y += 1
            x += 1
        game_time.calendar.render(VIEW_WIDTH + 2, 4)
        with term.location(VIEW_WIDTH+2, 6):
            print(hero.position)
        i = 1
        for line in range(i+6, VIEW_HEIGHT+6):
           with term.location(VIEW_WIDTH+1, line):
               print(term.clear_eol)

if __name__ == '__main__':
    import time
    import random
    import core
    import props
    import game_time
    import term_interpreter
    from title_screen import TitleScreen
    from undercoat import DynamicChunkMapGen, AreaGridChunkGen
    import adventure
    game = map_generators.battle_city(MapScene(), 200, 200, 400)
    adventure.current.scene = game
    adventure.current.revive_point = (game, game.hero.position)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        message.log.render(term)
        takeover(TitleScreen())
        title_message = [
            "Welcome to the world of MONS.",
            "Monsters are everywhere and you are one of them.",
            "Being a monster is great and fun.",
            "You are a special kind of monster.",
            "You are a COACH.",
            "You can only become stronger by making the monsters "+
            "around you become strong.",
            "Many MONs love to be strong and to FIGHT.",
            "Help the MONs that love to fight to become strong, and "+
            "succeed at the sport of competitive fighting.",
            "But be careful - you will need to build up the SELF-CONFIDENCE "+
            "of your comrades and earn their TRUST to succeed.",
            "Remember, each MON is different, and so are you.",
            "Good luck!",
            ]
        for msg in title_message:
            game.show_message(msg)
        game.render()
        message.log.render(term)
        while True:
            adventure.current.scene.update(term_interpreter.get_signal())
            adventure.current.scene.render()
            message.log.render(term)
            if adventure.current.scene.transition_with:
                next_scene = aventure.current.scene.transition_with
                adventure.current.scene.transition_with = None
                adventure.current.scene = next_scene
                adventure.current.scene.render()

