import random
import mon_species
import mon_states
from move_types import ATK, DEF, FIN

names = []
with open("names.txt") as f:
    for line in f:
        names.append(line.strip())
class Mon:
    def __init__(self, species):
        self.name = species.name + " " + random.choice(names)
        self.species = species
        self.type1 = self.species.type1
        self.type2 = self.species.type2
        self.trust = 4
        self.self_confidence = 4
        self.morale = 4
        self.level = 5
        self.attacks = []
        self.attack_cap = 4
        self.defences = []
        self.defence_cap = 3
        self.finishers = []
        self.finisher_cap = 2
        for move in species.basic_moves:
            if move.move_type.action == ATK:
                self.attacks.append(move)
            elif move.move_type.action == DEF:
                self.defences.append(move)
            elif move.move_type.action == FIN:
                self.finishers.append(move)
        self.unlearned_moves = list(species.learned_moves)
        body_type = random.choice((self.type1, self.type2))
        adj = random.choice(body_type.adjectives)
        self.body = mon_states.make_scale(mon_states.body, body_type, adj, 3)
        self.states = []
        speed = random.randint(5, 15)
        power = random.randint(5, 15)
        wisdom = random.randint(5, 15)
        tank = random.randint(5, 15)
        total = speed + power + wisdom + tank
        speedr = speed/total
        powerr = power/total
        wisdomr = wisdom/total
        tankr = tank/total
        self.speed = int(speedr*60)
        self.power = int(powerr*60)
        self.wisdom = int(wisdomr*60)
        self.tank = int(tankr*60)
        def_size = min(self.tank // 3, 6) 
        def_type = random.choice((self.type1, self.type2))
        scale_type, mon_type, adj = random.choice(species.state_templates)

if __name__ == "__main__":
    for i in range(20):
        s = mon_species.Species()
        m = Mon(s)
        print(m.name, m.species.description)
        print("power", m.power, "wisdom", m.wisdom, "tank", m.tank, "speed",
                m.speed)
