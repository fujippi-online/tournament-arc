import geometry
import sys

class Tile:
    def __init__(self, symbol, name, blocks = False, clear = True, like = None,
            color = 'bright_white'):
        self.symbol = symbol
        self.name = name
        self.blocks = blocks
        self.clear = clear
        self.color = color
        assert len(symbol) == 1
        if like:
            self.blocks = like.blocks
            self.clear = like.clear
t_blank = Tile(" ", "Nothingness", clear = True, blocks = False)
t_dark = Tile(" ", "Darkness", clear = False, blocks = True, color = "black_on_black")
t_wall = Tile("#", "Wall", clear = False, blocks = True)
t_window = Tile("#", "Glass", clear = True, blocks = True, color =
        "bright_blue")
t_water = Tile("~", "Water", clear = True, blocks = True, color =
        "bright_blue_on_blue")
t_rock = Tile("0", "Rock", like=t_wall, color = "black_on_yellow")
t_post = Tile("|", "Gatepost", like=t_wall, color = "yellow")
t_tree = Tile("T", "Tree", like=t_wall, color = "black_on_green")
t_tree2 = Tile("T", "Tree", like=t_wall, color = "black_on_green")
t_tree3 = Tile("T", "Tree", like=t_wall, color = "black_on_green")
t_floor = Tile(".", "Floor")
t_blood = Tile(".", "Blood", like = t_floor, color = "red")
t_grass = Tile("\"", "Grass", like = t_floor, color = "green")
t_grass2 = Tile("\"", "Grass", like = t_floor, color = "green")
t_flower = Tile("*", "Flower", like = t_floor, color = "pink")
t_dirt = Tile(".", "Dirt", like = t_floor, color = "yellow")
t_moss = Tile(".", "Moss", like = t_floor, color = "green")
t_moss2 = Tile(".", "Moss", like = t_floor, color = "green")
t_road = Tile(".", "Road", like = t_floor, color = "white")
t_1 = Tile("1", "1", like = t_floor, color = "green")
t_2 = Tile("2", "2", like = t_floor, color = "green")
t_3 = Tile("3", "3", like = t_floor, color = "green")
t_4 = Tile("4", "4", like = t_floor, color = "green")
t_5 = Tile("5", "5", like = t_floor, color = "green")
t_6 = Tile("6", "6", like = t_floor, color = "green")
t_7 = Tile("7", "7", like = t_floor, color = "green")
t_8 = Tile("8", "8", like = t_floor, color = "green")
t_9 = Tile("9", "9", like = t_floor, color = "green")

class Map:
    def __init__(self):
        self.tiles = {}
    def submap(self, x, y, w, h):
        tiles = [] 
        for i in range(x, x+w):
            col  = []
            for j in range(y, y+h):
                col.append(self[(i,j)])
            tiles.append(col)
        return tiles
    def __getitem__(self, key):
        try: 
            return self.tiles[key]
        except KeyError:
            return t_blank
    def get_bounds(self):
        """
        Return a rect respresenting the map's bounds.
        """
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = -sys.maxsize
        max_y = -sys.maxsize
        for point in self:
            x, y = point
            if x > max_x: max_x = x
            if x < min_x: min_x = x
            if y > max_y: max_y = y
            if y < min_y: min_y = y
        return (min_x, min_y, max_x - min_x, max_y - min_y)
    def draw_line(self, tile, p1, p2):
        """
        Draw a line on the map.
        """
        for p in geometry.iter_line(p1, p2):
            self.tiles[p] = tile
    def adjacent(self, point):
        x, y = point
        nearby_spaces = [
                (0,1),
                (1,0),
                (0,-1),
                (-1,0),
                (1,-1),
                (1,1),
                (-1,1),
                (-1, -1),
                ]
        adj_points = []
        for dx, dy in nearby_spaces:
            p2 = (x+dx, y+dy)
            if self[p2].blocks == False:
                adj_points.append(p2)
        return adj_points
    def closest_free_point(self, point):
        neighbours = self.adjacent(point)
        while True:
            for p in neighbours:
                if not self[p].blocks:
                    return p
            new_neighbours = [self.adjacent(p) for p in neighbours]
            neighbours = list([p for p in new_neighbours if p not in neighbours])
    def write_chunk(self, x, y, chunk):
        for dy, row in enumerate(chunk):
            for dx, tile in enumerate(row):
                self.tiles[(x+dx, y+dy)] = tile
    def draw_rect(self, tile, rect):
        """
        Draw the outline of a rect on the map.
        """
        x, y, w, h = rect
        x2 = x+w
        y2 = y+h
        points = [
                (x, y),
                (x2, y),
                (x2, y2),
                (x, y2),
        ]
        lines = [(points[i], points[i+1]) for i in range(3)] 
        lines.append((points[-1], points[0]))
        for line in lines:
            p1, p2 = line
            self.draw_line(tile, p1, p2)
    def fill_rect(self, tile, rect):
        x, y, w, h = rect
        for tx in range(x, x + w):
            for ty in range(y, y + h):
                self.tiles[(tx, ty)] = tile

