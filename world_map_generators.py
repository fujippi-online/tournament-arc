"""
Generate the layout of chunks in the area grid that controls the world map.
"""
import road.map_generators
from undercoat import DynamicChunkMapGen, AreaGridChunkGen
from forest.map_generators import random_trees, random_forest_block
from town.map_generators import town_block
from cave.map_generators import hideout_entrance

def test_map(scene):
    world_map = AreaGridChunkGen(random_forest_block)
    world_generator = DynamicChunkMapGen(world_map)
    scene.undercoat.append(world_generator)
    road_block = road.map_generators.RoadChunkGenerator(random_trees, world_map) 
    world_map.draw_rect(road_block,-10,0,20,0)
    world_map.draw_rect(road_block,0,-2,0,20)
    world_map.draw_rect(town_block,-2,-7,5,5)
    world_map.draw_rect(town_block,-2,-7,5,5)
    world_map.draw_point(hideout_entrance, 1, 1)
    world_generator.update(scene)
    return world_map

def endless_town(scene):
    world_map = AreaGridChunkGen(town_block)
    world_generator = DynamicChunkMapGen(world_map)
    scene.undercoat.append(world_generator)
    road_block = road.map_generators.RoadChunkGenerator(random_trees, world_map) 
    world_map.draw_rect(road_block,0,-2,0,20)
    world_map.draw_rect(town_block,-2,-7,5,5)
    world_generator.update(scene)
    return world_map


