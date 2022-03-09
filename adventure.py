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
        self.monsters = []
        self.player_character = None
        self.current_map = None

def new_game():
    run = CurrentPlaythrough()
    run.types = random.sample(mon_types.types, k=10)
    for t in run.types:
        affected_types = random.sample(run.types, k=6)
        print(t.name)
        run.strong_vs[t] = affected_types[:3]
        print("Strong vs:")
        print(*tuple([i.name for i in run.strong_vs[t]]))
        run.resisted_by[t] = affected_types[3:]
        print("Resisted by:")
        print(*tuple([i.name for i in run.resisted_by[t]]))
        print(" ")
    return run

current = new_game()
