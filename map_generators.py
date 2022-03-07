import random
import string

from collections import defaultdict, deque

from pathing import path

import roguemap
import geometry
import door
import character
import message

def none_intersect(rects, r1):
    for r2 in rects:
        if geometry.intersects(r1, r2):
            return False
    return True

door_spots = set()
def is_doorway(background, position):
    x, y = position
    for adjacent_spot in background.adjacent(position):
        if adjacent_spot in door_spots:
            return False
    adj = set(background.adjacent(position))
    l = (x-1, y) in adj
    r = (x+1, y) in adj
    u = (x, y-1) in adj
    d = (x, y+1) in adj
    passable = (background[position].blocks == False) 
    num_adj = len(background.adjacent(position)) 
    surrounded = num_adj == 4 or num_adj == 3
    sandwich = (l and r) or (u and d)
    inverse_sandwich = (not l and not r) or (not u and not d)
    if passable and surrounded and sandwich and inverse_sandwich:
        door_spots.add(position)
    return passable and surrounded and sandwich and inverse_sandwich

class Room:
    def __init__(self, rect):
        self.rect = rect
        self.door_locations = []
    def place(self, scene):
        scene.background.fill_rect(roguemap.t_floor, self.rect)
        scene.background.draw_rect(roguemap.t_wall, self.rect)
        for p in self.door_locations:
            scene.background.tiles[p] = roguemap.t_floor
            scene.foreground.append(door.Door(*p))

class Passage:
    def __init__(self, p1, p2, width = 1):
        self.p1 = p1
        self.p2 = p2
        self.width = width
    def place(self, scene):
        width = self.width
        p1, p2 = self.p1, self.p2
        x1, y1 = p1
        x2, y2 = p2
        vx, vy = (x1-x2, y1 - y2)
        ux, uy = geometry.normalize((-vy, vx)) #perpendicular
        p1_start = (int(x1 - ux*width), int(y1 - uy*width))
        p1_end = (int(x1 + ux*width), int(y1 + uy*width))
        p2_start = (int(x2 - ux*width), int(y2 - uy*width))
        p2_end = (int(x2 + ux*width), int(y2 + uy*width))
        line1 = geometry.iter_line(p1_start, p1_end)
        line2 = geometry.iter_line(p2_start, p2_end)
        for line_start, line_end in zip(line1, line2):
            scene.background.draw_line(roguemap.t_floor,
                    line_start, line_end)
        scene.background.draw_line(roguemap.t_wall, p1_start, p2_start)
        scene.background.draw_line(roguemap.t_wall, p1_end, p2_end)


def single_level_dungeon(scene, width, height, num_rooms):
    min_room_width = 7
    min_room_height = 6
    max_room_width = 20
    max_room_height = 15
    min_passage_translation = 2
    max_passage_translation = 10
    rooms = []
    room_areas = []
    passages = []
    rooms_planned = 0
    scene.background.fill_rect(roguemap.t_wall, (-2, -2, width, height))
    while rooms_planned < num_rooms:
        x = random.randint(0, width)
        y = random.randint(0, height)
        w = random.randint(min_room_width, max_room_width)
        h = random.randint(min_room_height, max_room_height)
        r = (x,y,w,h)
        if none_intersect(room_areas, geometry.grow(r,2)):
            room_areas.append(r)
            print geometry.grow(r,2), r
            rooms_planned += 1
            print rooms_planned
        else: print "discarded", r
    for rect in room_areas:
        room = Room(rect)
        rooms.append(room)
    for room in rooms:
        closest_room = None
        closest_distance = width*height
        for other_room in rooms:
            if other_room == room: continue
            dist = geometry.rect_distance(room.rect, other_room.rect)
            if dist < closest_distance:
                closest_room = other_room
                closest_distance = dist
        door1, door2 = geometry.rect_closest_points(room.rect, closest_room.rect)
        room.door_locations.append(door1)
        closest_room.door_locations.append(door2)
        passages.append(Passage(door1, door2, width=2))
        print room.rect, closest_room.rect, door1, door2
    for passage in passages:
        passage.place(scene)
    for room in rooms:
        room.place(scene)
    start_room = random.choice(rooms)
    hx, hy = geometry.rect_center(start_room.rect)
    scene.hero.x, scene.hero.y = hx, hy
    scene.camera.center_on(scene.hero)
    return scene

def box_o_boxes(scene, width, height, num_boxes):
    foreground = []
    background = roguemap.Map()
    boxes_left = num_boxes
    placed_boxes = []
    background.fill_rect(roguemap.t_floor, (0, 0, width, height))
    background.draw_rect(roguemap.t_wall, (0, 0, width, height))
    rint = random.randint
    while boxes_left > 0:
        box = (rint(1, width),
                rint(1, height),
                rint(2,9),
                rint(2,9)) 
        if none_intersect(placed_boxes, box) and\
                not geometry.point_in_rect(box, (5,5)):
            placed_boxes.append(box)
            boxes_left -= 1
            background.draw_rect(roguemap.t_wall, box)
    p = rint(1, height), rint(1,width)
    blood_path = path(background,(5,5), p)
    tries = 1
    while not blood_path:
        p = rint(10, height), rint(10,width)
        blood_path = path(background,(5,5), p)
        tries += 1
        print tries
    for point in blood_path:
        background.tiles[point] = roguemap.t_blood
    for i in range(1, width):
        for j in range(1, height):
            if is_doorway(background, (i, j)):
                foreground.append(door.Door(i,j))
    foreground.append(character.Monster(*blood_path[-1]))
    scene.foreground = foreground
    scene.background = background
    return scene
