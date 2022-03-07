from util import once

class Gatepoint:
    blocks = True
    clear = True
    def __init__(self, x, y, tx, ty, scene_generator, scene = None, 
            reverse = False):
        self.symbol = "*"
        self.x = x
        self.y = y
        self.encountered = False
        self.color = "white"
        self.bg_color = "black"
        self.scene = scene
        self.scene_generator = scene_generator
        self.tx, self.ty = tx, ty
        self.reverse = reverse
    def seen(self):
        if not self.encountered:
            self.encountered = True
    def interact(self, current_scene):
        if not self.scene:
            self.scene = self.scene_generator()
            # should add a handle to help find free exits from/to scenes
            # the following is pretty stopgap
            if not self.tx:
                self.tx, self.ty = self.scene.hero.position
            if self.reverse:
                self.scene.foreground.append(self.make_reverse(current_scene))
        current_scene.transition_with = self.scene
        self.scene.hero.x = tx
        self.scene.hero.x = ty
    def make_reverse(self, scene):
        return Gatepoint(self.tx, self.ty, self.x, self.y, lambda: scene)
    @property
    def position(self):
        return self.x, self.y

