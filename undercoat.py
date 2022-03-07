from collections import defaultdict, deque

import settings
import geometry
import message
import random

class DynamicChunkMapGen:
    """
    A map generator that runs continually and makes new chunks adjacent to 
    the hero's position.
    """
    def __init__(self, chunk_generator):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_generator = chunk_generator
        self.chunk_populated = defaultdict(lambda: False)
    def current_chunk(self, scene):
        x, y = scene.hero.position
        w, h = self.chunk_size
        return x/w, y/h
    def chunk_rect(self, chunk):
        ci, cj = chunk
        cw, ch = self.chunk_size
        return ci*cw, cj*ch, cw, ch
    def surrounding(self, position):
        x,y = position 
        nearby_spaces = [
                (0,0),
                (0,1),
                (1,0),
                (2,0),
                (-2,0),
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
            adj_points.append(p2)
        return adj_points
    def update(self, scene):
        if hasattr(self.chunk_generator, "generate"):
            generate = self.chunk_generator.generate
        else:
            generate = self.chunk_generator
        cc = self.current_chunk(scene)
        blank_neighbours = [c for c in self.surrounding(cc)
                if self.chunk_populated[c] == False]
        for neighbour in blank_neighbours:
            rect = self.chunk_rect(neighbour)
            generate(scene, rect)
            self.chunk_populated[neighbour] = True

class AreaGridChunkGen:
    """
    AreaGridMapGen(default_generator)
    This map generator delegates to other chunk-based map generators.
    There's one it uses by default, like the background in a bitmap, and others
    are "drawn" over the top in the form of rects.
    """
    def __init__(self, default_generator):
        self.default_generator = default_generator
        self.areas = deque()
    def generator_for(self,chunk):
        x,y,w,h = chunk
        chunk_point  = (x/w, y/h)
        for area, generator in self.areas:
            if geometry.point_in_rect(area, chunk_point):
                return generator
        return self.default_generator
    def draw_rect(self, generator, x, y, w, h):
        area = x, y, w, h
        self.areas.appendleft((area, generator))
    def draw_point(self, generator, x, y):
        area = x, y, 1, 1
        self.areas.appendleft((area, generator))
    def generate(self, scene, chunk):
        generator = self.generator_for(chunk)
        if hasattr(generator, "generate"):
            generate = generator.generate
        else:
            generate = generator
        generate(scene, chunk)

class WeightedChunkGen:
    def __init__(self, generic_chunks, unique_chunks):
        self.generic_chunks = generic_chunks
        self.unique_chunks = unique_chunks
        self.total_weight = 0.0
        for weight, generator in generic_chunks:
            self.total_weight += weight
        for weight, generator in unique_chunks:
            self.total_weight += weight
    def select_generator(self):
        index = random.random()*self.total_weight
        for weight, generator in self.generic_chunks:
            index -= weight
            if index <= 0:
                return generator
        final_generator = None
        final_weight = 0
        for weight, generator in self.unique_chunks:
            index -= weight
            if index <= 0:
                final_generator = generator
                final_weight = weight
                break
        final_element = (final_weight, final_generator)
        self.unique_chunks.remove(final_element)
        self.total_weight -= final_weight
        return final_generator
    def generate(self, scene, chunk):
        generator = self.select_generator()
        if hasattr(generator, "generate"):
            generate = generator.generate
        else:
            generate = generator
        generate(scene, chunk)


    
