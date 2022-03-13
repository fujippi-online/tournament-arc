import random
import geometry

def random_point_in_chunk(chunk):
    cx,cy,cw,ch = chunk
    tx = random.randint(cx, cx+cw-1)
    ty = random.randint(cy, cy+ch-1)
    return tx, ty

def free_point_in_chunk(scene, chunk):
    px, py = random_point_in_chunk(chunk)
    while scene.background[px, py].blocks:
        px, py = random_point_in_chunk(chunk)
    return px, py

def place_item(scene, chunk, item):
    x, y = free_point_in_chunk(scene, chunk)
    item.x, item.y = x, y
    scene.foreground.append(item)

def reposition_item(scene, chunk, item):
    x, y = free_point_in_chunk(scene, chunk)
    item.x, item.y = x, y

def scatter(scene, chunk, tile, amount):
    cx,cy,cw,ch = chunk
    for i in range(amount):
        tx, ty = random_point_in_chunk(chunk)
        if (tx, ty) != scene.hero.position:
            scene.background.tiles[(tx, ty)] = tile

def scatter_patches(scene, chunk, tile, size, amount):
    assert size >= 2
    cx,cy,cw,ch = chunk
    for i in range(amount):
        px, py = random_point_in_chunk(chunk)
        pw = random.randint(2, size)
        ph = random.randint(2, size)
        patch_rect = (px, py, pw, ph)
        if geometry.contains(chunk, patch_rect):
            scene.background.fill_rect(tile, patch_rect)

def nearby_free_point(scene, point, radius):
    free_points = [p for p in geometry.iter_circle(point, radius) 
            if not scene.background[p].blocks]
    return random.choice(free_points)

def variations(scene, chunk, tile, variations):
    options = [tile] + variations
    tiles = scene.background.tiles
    for point in geometry.iter_rect(chunk):
        if tiles[point] == tile:
            tiles[point] = random.choice(options)

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

def similar_adjacent(scene, point):
    x, y = point
    bg = scene.background
    nearby_spaces = [LEFT, RIGHT, UP, DOWN]
    return frozenset([(dx, dy) for dx, dy in nearby_spaces if bg[point] == bg[(x+dx, y + dy)] ])

def autotile(scene, chunk, target, auto_map):
    auto_map[frozenset([])] = target
    to_set = {}
    for x,y in geometry.iter_rect(chunk):
        if scene.background[(x,y)] == target:
            try:
                to_set[(x,y)] = auto_map[similar_adjacent(scene,(x,y))]
                #print similar_adjacent(scene, (x, y))
            except:
                pass
    for p in to_set:
        scene.background.tiles[p] = to_set[p]
