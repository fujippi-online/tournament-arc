import mon_types 
import random

class CurrentPlaythrough:
    def __init__(self):
        self.types = []
        self.party = []
        self.maps = []
        self.trophies = []
        self.monsters = []
        self.player_character = None
        self.current_map = None

def new_game():
    run = CurrentPlaythrough()
    run.types = random.choices(mon_types.types, k=10)
    return run

current = new_game()
