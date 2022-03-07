"""
Terrain-shaping barriers to place on the world map, such as mountains and sea.
"""
import roguemap as tiles
from map_util import (
        free_point_in_chunk, 
        place_item, 
        scatter,
        random_point_in_chunk)

def sea(scene, chunk):
    scene.background.draw_rect(tiles.t_water, chunk)
    scatter(scene, chunk, tiles.t_rock, 20)

def mountain(scene, chunk):
    scene.background.draw_rect(tiles.t_rock, chunk)
    scatter(scene, chunk, tiles.t_dirt, 50)

def dense_trees(scene, chunk):
    scene.background.draw_rect(tiles.t_tree, chunk)
    scatter(scene, chunk, tiles.t_dirt, 50)
