import time 

import message
import geometry
import tiles
import settings
import palette
from core import DIRECTIONS, term

DONE = object()
class NoKey:
    code = None
    name = "NO_KEY"

def takeover(game_process):
    if settings.ENGINE_MODE == "TERM":
        return term_takeover(game_process)
    elif settings.ENGINE_MODE == "SDL":
        return sdl_takeover(game_process)

def term_takeover(game_process):
    print(term.clear)
    result = game_process.update(NoKey())
    if hasattr(game_process, "initial_render"):
        game_process.initial_render()
    game_process.render()
    message.log.render(term)
    while result == None:
        key = term.inkey()
        result = game_process.update(key)
        game_process.render()
        message.log.render(term)
    return result


def tag_key(term, key):
    for key_name in DIRECTIONS.keys():
        if key.code == getattr(term, key_name):
            return key_name
        elif key_name == key:
            return key_name

class TargetPicker:
    def __init__(self, scene, box = None):
        self.scene = scene
        self.cursor_pos = scene.hero.position
        self.box = box
    def update(self, key):
        cx, cy = self.cursor_pos
        key_name = None
        if key.name:
            key_name = key.name
        if not key_name:
            key_name = tag_key(term, key)
        if key_name and key_name in DIRECTIONS:
            dx, dy = DIRECTIONS[key_name]
            if self.box:
                max_dx, max_dy = self.box
                allowed_rect = (
                        self.scene.hero.x - max_dx,
                        self.scene.hero.y - max_dy,
                        max_dx*2,
                        max_dy*2)
                new_cursor_pos = (cx + dx, cy + dy)
                if geometry.point_in_rect(allowed_rect, new_cursor_pos):
                    self.cursor_pos = new_cursor_pos
            else:
                self.cursor_pos = (cx + dx, cy + dy)
        elif key_name == "KEY_ENTER" or key_name == "confirm":
            self.highlight.select()
            if settings.ENGINE_MODE == "SDL":
                animate(self, settings.FPS/4)
            return self.cursor_pos
    def render(self):
        self.scene.render()
        camera = self.scene.camera
        with term.location(*camera.adjust(*self.cursor_pos)):
            print term.white_on_white("_")



