import message
import geometry
import settings

from control import tag_key
from core import DIRECTIONS, term

class Inspector:
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
        elif key_name == "KEY_ENTER" or key == "q":
            return self.cursor_pos
    def render(self):
        scene = self.scene
        scene.render()
        camera = scene.camera
        with term.location(*camera.adjust(*self.cursor_pos)):
            print(term.white_on_white("_"))
        if scene.visible(scene.hero.position, self.cursor_pos):
            self.render_stack()
    def render_stack(self):
        scene = self.scene
        current_tile = scene.background[self.cursor_pos]
        things_on_tile = scene.things_at(*self.cursor_pos)
        x = settings.VIEW_WIDTH + 2
        with term.location(x, 2):
            color = getattr(term, current_tile.color)
            print(color(current_tile.symbol)+" "+
                    current_tile.name+term.clear_eol)
        for y, thing in enumerate(things_on_tile):
            with term.location(x, y+3):
                if hasattr(thing, "name"):
                    color = getattr(term, thing.color, term.white)
                    print(color(thing.symbol)+" "+thing.name+term.clear_eol)
        for y in range(len(things_on_tile)+3, settings.VIEW_HEIGHT):
            with term.location(x,y):
                print(term.clear_eol)


