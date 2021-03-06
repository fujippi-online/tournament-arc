import mon_types 
import random

class CurrentPlaythrough:
    def __init__(self):
        self.types = []
        self.party = []
        self.maps = []
        self.strong_vs = {}
        self.resisted_by = {}
        self.trophies = []
        self.mons = []
        self.map_party = []
        self.player_character = None
        self.current_map = None
        self.revive_point = None #(revive_scene, (x, y))
        self.scene = None

party_limit = 5

def new_game():
    run = CurrentPlaythrough()
    print("Generating types...")
    run.types = random.sample(mon_types.types, k=10)
    for t in run.types + [mon_types.coach]:
        affected_types = random.sample(run.types, k=6)
        run.strong_vs[t] = affected_types[:3]
        run.resisted_by[t] = affected_types[3:]
    return run

current = new_game()


import mon_species
import mons
def generate_mons():
    print("Generating mons...")
    for i in range(150):
        current.mons.append(mon_species.Species())
    for i in range(4):
        current.party.append(mons.Mon(random.choice(current.mons)))
generate_mons()
