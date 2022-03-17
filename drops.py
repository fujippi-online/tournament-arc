"""
System for managing dropped items, dropped knowledge, distributed NPCs.
For allowing map generators to create things that might appear elsewhere in the
world, thus allowing the kind of interconnectedness that the game would
otherwise lack. This is the focus of drops here, rather than the economic
distribution of in-game resources.
"""

import random

common = 10
uncommon = 5
rare = 1
super_rare = 0.1

class DropRegister:
    """
    Tracks droppable items.
    """
    def __init__(self):
        self.drops = []
        self.total_weight = 0
    def add(self, generator, rarity, limit = None):
        self.drops.append((generator, rarity, limit))
        self.total_weight += rarity
    def gen_drop(self):
        index = random.random()*self.total_weight
        current_weight = 0
        for generator, weight, limit in self.drops:
            current_weight += weight
            if current_weight > index:
                if limit != None:
                    self.drops.remove((generator, weight, limit))
                    if limit > 1:
                        self.drops.append((generator, weight, limit-1))
                    else:
                        self.total_weight -= weight
                if callable(generator):
                    return generator()
                else:
                    return generator

loot = DropRegister()
keys = DropRegister()

def test_drops():
    test_stuff = DropRegister()
    test_stuff.add(lambda: "a")
    assert test_stuff.total_weight == common
    test_stuff.add(lambda: "b")
    assert test_stuff.total_weight == common*2
    test_stuff.add(lambda: "c", limit = 1) 
    results = [test_stuff.gen_drop() for i in range(100)]
    for result in results:
        assert result in ["a", "b", "c"]
    assert results.count("c") <= 1
    if results.count("c") == 1:
        assert test_stuff.total_weight == common*2

