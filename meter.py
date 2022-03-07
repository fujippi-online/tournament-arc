from core import term
class Meter:
    def __init__(self, name, current, maximum, position, color = "white"):
        self.maximum = maximum
        self.current = current
        self.name = name
        self.color = color
        self.x, self.y = position
    @property
    def portion(self):
        return float(self.current)/float(self.maximum)
    @property
    def used(self):
        return self.maximum - self.current
    def render(self):
        color = getattr(term, self.color)
        with term.location(self.x, self.y):
            print((str(self.name)+": "+str(self.current)+"/"+str(self.maximum)))
        if self.maximum < 10:
            with term.location(self.x, self.y+1):
                print((color("="*self.current)+term.bright_black("-"*self.used)))
        else:
            remaining = int(self.portion*10)
            used = 10 - remaining
            with term.location(self.x, self.y+1):
                print((color("="*remaining)+term.bright_black("-"*used)))
    def __iadd__(self, other):
        self.current += other
        return self
    def __isub__(self, other):
        self.current -= other
        if self.current < 0: self.current = 0
        return self
