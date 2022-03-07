class Camera:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def adjust(self, wx, wy):
        return wx - self.x, wy - self.y
    def invert(self, sx, sy):
        return sx + self.x, sy + self.y
    def center_on(self, entity):
        dx = int(self.w/2)
        dy = int(self.h/2)
        self.x = entity.x - dx
        self.y = entity.y - dy
    @property
    def position(self):
        return self.x, self.y
    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)
