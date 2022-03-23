from util import once
import message
import adventure

class Gatepoint:
    blocks = True
    clear = False
    def __init__(self, p_from, p_to, scene):
        self.symbol = "_"
        x,y = p_from
        self.x = x
        self.y = y
        self.encountered = False
        self.color = "white"
        self.bg_color = "black"
        self.scene = scene
        self.tx, self.ty = p_to
    def seen(self):
        if not self.encountered:
            self.encountered = True
    def interact(self, current_scene):
        adventure.current.scene = self.scene
        adventure.current.scene.hero.x = self.tx
        adventure.current.scene.hero.y = self.ty
        self.scene.camera.center_on(self.scene.hero)
        self.scene.render()
    def make_reverse(self, scene):
        return Gatepoint((self.tx, self.ty), (self.x, self.y), scene)
    @property
    def position(self):
        return self.x, self.y

