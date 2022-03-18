import random

import drops
from inventory import Item

class Loot(Item):
    symbol = "0"
    color = "yellow"
    blocks = True
    def __init__(self, loot_type, adj, value, position = (0,0)):
        super().__init__(position = position)
        self.loot_type = loot_type
        self.adjective = adj
        self.value = value
        self.name = f"{adj} {loot_type}"

city_loot = drops.DropRegister()
jewelery_types = [
        "necklace",
        "earrings",
        "bracelet",
        "pendant",
        "watch",
       "pocketwatch",
        "coin",
    ]
expensive_jewelery_adjectives = [
        "bronze",
        "golden",
        "silver",
        "rosegold",
        "jewel-encrusted",
        ]
cheap_jewelery_adjectives = [
        "fake gold",
        "plastic",
        "rusty",
        "stainless steel"
        ]
def cheap_jewels():
    adj = random.choice(cheap_jewelery_adjectives)
    item = random.choice(jewelery_types)
    value = random.randint(1,10)*5
    return Loot(item, adj, value)
def expensive_jewels():
    adj = random.choice(expensive_jewelery_adjectives)
    item = random.choice(jewelery_types)
    value = random.randint(1,10)*5
    return Loot(item, adj, value)
city_loot.add(expensive_jewels, drops.common)
city_loot.add(cheap_jewels, drops.rare)
