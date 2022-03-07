"""
System for managing dropped items, dropped knowledge, distributed NPCs.
For allowing map generators to create things that might appear elsewhere in the
world, thus allowing the kind of interconnectedness that the game would
otherwise lack. This is the focus of drops here, rather than the economic
distribution of in-game resources.
"""

import random

class Rarity:
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
    def add(self, generator, weight = Rarity.common, limit = None):
        self.drops.append((generator, weight, limit))
        self.total_weight += weight
    def select_drop(self):
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
                return generator()

outdoor_items = DropRegister()
dungeon_items = DropRegister()
domestic_items = DropRegister()
treasure_chests = DropRegister()

friendly_conversations = DropRegister()
monster_conversations = DropRegister()

friendly_npcs = DropRegister()
outdoor_monsters = DropRegister()

def test_drops():
    test_stuff = DropRegister()
    test_stuff.add(lambda: "a")
    assert test_stuff.total_weight == Rarity.common
    test_stuff.add(lambda: "b")
    assert test_stuff.total_weight == Rarity.common*2
    test_stuff.add(lambda: "c", limit = 1) 
    results = [test_stuff.select_drop() for i in range(100)]
    for result in results:
        assert result in ["a", "b", "c"]
    assert results.count("c") <= 1
    if results.count("c") == 1:
        assert test_stuff.total_weight == Rarity.common*2

