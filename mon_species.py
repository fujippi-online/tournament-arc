import nltk
import random
import operator

import adventure
import mon_types
import move_types
import mon_bodies
import mon_states
import profanityfilter

from move_generator import generate_atk, generate_def, generate_fin
from move_generator import find_attacks, find_defences, find_finishers

syllable = nltk.tokenize.sonority_sequencing.SyllableTokenizer()
# hopefully this will prevent it from accidentally naming any mon a slur
detect_slurs = profanityfilter.ProfanityFilter()
class Species:
    def __init__(self, types = None):
        self.name = None
        self.description = None
        self.type1 = None
        self.type2 = None
        self.family = None
        self.variety = None
        self.basic_moves = []
        self.state_templates = []
        self.level_up_sequence = []
        self.generate(types = types)
    def generate(self, types = None):
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
        if types:
            self.type1, self.type2 = types
        else:
            self.type1 = random.choice(adventure.current.types)
            self.type2 = random.choice(adventure.current.types)
        self.family = random.choice(mon_bodies.body_types)
        self.variety = random.choice(self.family.varieties)
        clean = False
        while not clean:
            words = self.type1.nouns + self.type2.nouns + [self.variety]
            w1 = syllable.tokenize(random.choice(words).replace(" ",""))
            words += self.family.limbs
            w2 = syllable.tokenize(random.choice(words).replace(" ",""))
            while w1[0] == w2[0]:
                w2 = syllable.tokenize(random.choice(words))
            max_w1 = min(len(w1), 2)
            max_w2 = min(len(w2), 2)
            w1_amt = random.randint(1, max_w1)
            w2_amt = random.randint(1, max_w2)
            word1 = "".join(w1[:w1_amt])
            word2 = "".join(w2[-w2_amt:])
            self.name = (word1+word2).capitalize().replace(" ", "")
            clean = detect_slurs.is_clean(self.name)
        if "".join(w1) != self.variety:
            descriptor = "".join(w1)
        else:
            descriptor = random.choice(self.type1.nouns + self.type2.nouns)
        adj = random.choice(self.type1.adjectives + self.type2.adjectives)
        self.description = (f"The {adj} {descriptor} {self.variety}")
        t1_atks = find_attacks(self.type1, self.type1)
        if len(t1_atks) < 20:
            for power in range(1, 16):
                generate_atk(self.type1, self.type1, power = power)
            t1_atks = find_attacks(self.type1, self.type1)
        t2_atks = find_attacks(self.type2, self.type2)
        if len(t2_atks) < 20:
            for power in range(1, 16):
                generate_atk(self.type2, self.type2, power = power)
            t2_atks = find_attacks(self.type2, self.type2)
        t12_atks = find_attacks(self.type1, self.type2)
        if len(t12_atks) < 20:
            for power in range(1, 16):
                generate_atk(self.type1, self.type2, power = power)
            t12_atks = find_attacks(self.type1, self.type2)
        t21_atks = find_attacks(self.type2, self.type1)
        if len(t21_atks) < 20:
            for power in range(1, 16):
                generate_atk(self.type1, self.type2, power = power)
            t21_atks = find_attacks(self.type1, self.type2)
        t1_defs = find_defences(self.type1, self.type1)
        if len(t1_defs) < 20:
            for tank in range(1, 16):
                generate_def(self.type1, self.type1, power = tank)
            t1_defs = find_defences(self.type1, self.type1)
        t2_defs = find_defences(self.type2, self.type2)
        if len(t2_defs) < 20:
            for tank in range(1, 16):
                generate_def(self.type2, self.type2, power = tank)
            t2_defs = find_defences(self.type2, self.type2)
        t12_defs = find_defences(self.type1, self.type2)
        if len(t12_defs) < 20:
            for tank in range(1, 16):
                generate_def(self.type1, self.type2, power = tank)
                generate_def(self.type1, self.type2, power = tank)
            t12_defs = find_defences(self.type1, self.type2)
        t21_defs = find_defences(self.type2, 16)
        if len(t21_defs) < 20:
            for tank in range(1, 16):
                generate_def(self.type2, self.type1, power = tank)
                generate_def(self.type2, self.type1, power = tank)
            t21_defs = find_defences(self.type2, self.type1)
        t1_fins = find_finishers(self.type1, self.type1)
        if len(t1_fins) < 20:
            for power in range(1, 16):
                generate_fin(self.type1, self.type1, power = power)
            t1_fins = find_finishers(self.type1, self.type1)
        t2_fins = find_finishers(self.type2, self.type2)
        if len(t2_fins) < 20:
            for power in range(1, 15):
                generate_fin(self.type2, self.type2, power = power)
            t2_fins = find_finishers(self.type2, self.type2)
        t12_fins = find_finishers(self.type1, self.type2)
        if len(t12_fins) < 20:
            for power in range(1, 15):
                generate_fin(self.type1, self.type2, power = power)
            t12_fins = find_finishers(self.type1, self.type2)
        t21_fins = find_finishers(self.type2, self.type1)
        if len(t21_fins) < 20:
            for power in range(1, 15):
                generate_fin(self.type1, self.type2, power = power)
            t21_fins = find_finishers(self.type1, self.type2)
        atks = t1_atks + t2_atks + t12_atks + t21_atks
        defs = t1_defs + t2_defs + t12_defs + t21_defs
        fins = t1_fins + t2_fins + t12_fins + t21_fins
        atk_pow = 1
        def_pow = 1
        used_moves = set()
        level = 6
        skips =  0
        while level <= 50 and skips < 10:
            atk_ratio = (def_pow*self.power)/(atk_pow*self.tank)
            if random.random() < atk_ratio:
                try:
                    power = atk_pow//3 + 1
                    poss_atks = [a for a in atks if (a.power == power or
                            a.power == power-1) and a not in used_moves]
                    poss_fins = [a for a in fins if (a.power == power or
                            a.power == power - 1) and a not in used_moves]
                    poss = poss_atks + poss_fins
                    random.shuffle(poss)
                    choice1 = poss.pop()
                    choice2 = poss.pop()
                    used_moves.add(choice1)
                    used_moves.add(choice2)
                    self.level_up_sequence.append((choice1, choice2))
                except IndexError:
                    skips += 1
                atk_pow += 1
            else:
                try:
                    power = def_pow//3 + 1
                    poss = [a for a in defs if (a.power == power or 
                            a.power == power - 1) and a not in used_moves]
                    random.shuffle(poss)
                    choice1 = poss.pop()
                    choice2 = poss.pop()
                    used_moves.add(choice1)
                    used_moves.add(choice2)
                    self.level_up_sequence.append((choice1, choice2))
                except IndexError:
                    skips += 1
                def_pow += 1
                self.level_up_sequence.append((choice1, choice2))
            level += 1
        for i in range(5): 
            mon_type = random.choice([self.type1, self.type2])
            scale_type = random.choice(mon_states.scale_types)
            adj = random.choice(mon_type.adjectives + mon_type.nouns)
            self.state_templates.append((scale_type, mon_type, adj))
        atks_left = sorted([a for a in atks if a not in used_moves], 
                key = operator.attrgetter("power"), reverse = True)
        defs_left = sorted([a for a in defs if a not in used_moves], 
                key = operator.attrgetter("power"), reverse = True)
        fins_left = sorted([a for a in fins if a not in used_moves], 
                key = operator.attrgetter("power"), reverse = True)
        self.basic_moves = [
                atks_left.pop(),
                defs_left.pop(),
                atks_left.pop(),
                defs_left.pop(),
                fins_left.pop()]
        

if __name__ == "__main__":
    for i in range(100):
        s = Species()
        print(s.name)
        print(s.description)
        print(*tuple(set([s.type1.name, s.type2.name])))
        for armour in s.state_templates:
            st, mt, adj = armour
            print(adj, st.name)
        for move in s.basic_moves:
            print(move.name)
        print(" ")
