import random
import math
import time

import rpack

import adventure
import geometry
import cast
import battle
import mons
import drops
import door
import map_util
import loot
import roguemap
from map_scene import MapScene
from core import term

# API ScenePart which given generate(scene,x,y) fills 
# (x,y,self.width,self.height) with the randomized contents given.
# computes width, height on init by calling plan()
# and can recompute by re-calling plan
# idea being that rather than fitting the parts to the scene, we can instead
# build scenes as an arangement of parts, which allows using the drop system
# for entire building, structures, etc
town_parts = drops.DropRegister()
class House:
    def __init__(self, rooms):
        """
        rooms: a list of things to be placed in each room
        """
        self.width = 0
        self.height = 0
        self.rooms = rooms
        self.room_boxes = []
        self.door_points = []
        front_door = None
        self.plan()
    def plan(self):
        main_room = (0, 0, random.randint(6,10), random.randint(6,10))
        self.room_boxes.append(main_room)
        self.front_door = random.choice(geometry.side_middles(main_room))
        for room in self.rooms:
            while True:
                buddy_box = random.choice(self.room_boxes)
                other_boxes = list([box for box in self.room_boxes 
                    if box != buddy_box]) 
                door_proposal = self.front_door
                while door_proposal == self.front_door:
                    door_proposal = random.choice(
                            geometry.side_middles(buddy_box))
                    dx, dy = door_proposal
                bx, by, bw, bh = buddy_box
                w = random.randint(3,6)
                h = random.randint(3,6)
                if dx == bx:
                    x = bx - w
                elif dx == bx+bw:
                    x = dx
                else:
                    x = dx - (w//2)
                if dy == by:
                    y = by - h
                elif dy == by+bh:
                    y = dy
                else:
                    y = dy - (h//2)
                box = (x, y, w, h)
                possible_match = True
                for other in other_boxes:
                    if geometry.intersects(box, other):
                        possible_match = False
                if possible_match:
                    self.room_boxes.append(box)
                    self.door_points.append(door_proposal)
                    break
        #calc offset to normalize origin to 0,0
        min_x = 0
        min_y = 0
        for box in self.room_boxes:
            x,y,w,h = box
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
        # normalize
        new_positions = []
        for box in self.room_boxes:
            x,y,w,h = box
            new_positions.append((x-min_x, y-min_y, w, h))
        self.room_boxes = new_positions
        new_positions = []
        for door in self.door_points:
            x,y = door
            new_positions.append((x-min_x, y-min_y))
        self.door_points = new_positions
        x,y = self.front_door
        self.front_door = (x-min_x, y-min_y)
        # calc width
        for box in self.room_boxes:
            x,y,w,h = box
            if x < 0 or y < 0:
                print(box)
            if x+w > self.width:
                self.width = x+w
            if y+h > self.height:
                self.height = y+h
    def generate(self, scene, x, y):
        for items, box in zip(self.rooms, self.room_boxes):
            bx, by, bw, bh = box
            box_pos = (bx+x, by+y, bw, bh)
            scene.background.fill_rect(roguemap.t_floor, box_pos)
            scene.background.draw_rect(roguemap.t_wall, box_pos)
            for item in items:
                map_util.place_item(scene, box_pos, item)
        for dx, dy in self.door_points:
            door_pos = (dx+x, dy+y)
            scene.background.tiles[door_pos] = roguemap.t_floor
            scene.foreground.append(door.Door(*door_pos))
        dx, dy = self.front_door
        scene.background.tiles[(dx+x, dy+y)] = roguemap.t_floor
        fd = door.Door(dx+x, dy+y)
        fd.color = "red"
        scene.foreground.append(fd)

class Park:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.plan()
    def plan(self):
        self.pool_width = self.width//3
        self.pool_height = self.width//3
    def generate(self, scene, x, y):
        area = (x, y, self.width, self.height)
        center = geometry.rect_center(area)
        scene.background.fill_rect(roguemap.t_grass, area)
        num_flowers = self.width
        map_util.scatter(scene, area, roguemap.t_flower, num_flowers)
        shore_w = self.pool_width + 2
        shore_h = self.pool_width + 2
        pool_rect = geometry.rect_centered_on(center, 
                self.pool_width, self.pool_height)
        shore_rect = geometry.rect_centered_on(center, shore_w, shore_h) 
        scene.background.fill_rect(roguemap.t_dirt, shore_rect)
        scene.background.fill_rect(roguemap.t_water, pool_rect)

# API SceneGenerator
# class which provides generate(scene), which fills the given MapScene
# with the given contents and link tile spots in left_exit, right_exit, up_exit
# and down_exit which are None if there's no possible exit in that direction.

class ZonePacker:
    def __init__(self, required_zones, zone_gen, size = None, 
            ground = roguemap.t_dirt, scatter = None,
            border = roguemap.t_tree):
        self.ground = ground
        self.border = border
        if not scatter:
            self.scatter = []
        else:
            self.scatter = scatter
        if not size:
            size = len(required_zones)
        else:
            self.size = size
        to_gen = self.size - len(required_zones)
        generated_zones = []
        for x in range(to_gen):
            generated_zones.append(zone_gen.gen_drop())
        self.zones = required_zones + generated_zones
        self.plan()
    def plan(self):
        print("Planning map by packing zones...")
        random.shuffle(self.zones)
        sizes = list([(z.width+2, z.height+2) for z in self.zones])
        positions = rpack.pack(sizes)
        self.zone_positions = positions
        self.width, self.height = rpack.bbox_size(sizes, positions)
        map_box = (0,0,self.width, self.height)
        exits = geometry.side_middles(map_box)
        self.up_exit, self.left_exit, self.right_exit, self.down_exit = exits
    def generate(self):
        print("Generating zones...")
        scene = MapScene()
        map_box = (0,0,self.width, self.height)
        scene.background.fill_rect(self.ground, map_box)
        for tile, amt in self.scatter:
            map_util.scatter(scene, map_box, tile, amt)
        scene.background.draw_rect(self.border, map_box)
        for position, zone in zip(self.zone_positions, self.zones):
            x, y = position
            zone.generate(scene, x+1, y+1)
        map_util.reposition_item(scene, map_box, scene.hero)
        return scene

city_zones = drops.DropRegister() 
def battle_house():
    flag = battle.BattleTeam()
    leader_mon = mons.Mon(random.choice(adventure.current.mons))
    team_mons = [mons.Mon(random.choice(adventure.current.mons))
            for i in range(random.randint(1,3))]
    team = list([battle.BattleMember(0,0,mon,flag) for mon in team_mons])
    team.append(battle.BattleLeader(0,0,leader_mon,flag))
    return House(list([(npc, loot.city_loot.gen_drop()) for npc in team]))
city_zones.add(battle_house, drops.common)

def city_park():
    return Park(random.randint(12,25), random.randint(10,25))
city_zones.add(city_park, drops.rare)
test_city = ZonePacker([], city_zones, size = 100)

# CountryMap generates the world map for one country, filling its w,h sized
# grid with SceneGenerators and then when generate() is called, makes all the
# maps in the grid, joins them together and returns them in a list 
