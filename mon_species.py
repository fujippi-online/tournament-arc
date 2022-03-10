import nltk
import random

import mon_types
import move_types
import mon_bodies
import mon_states
import adventure
import profanityfilter

from move_generator import generate_atk, generate_def, generate_fin

syllable = nltk.tokenize.sonority_sequencing.SyllableTokenizer()
# hopefully this will prevent it from accidentally naming any mon a slur
detect_slurs = profanityfilter.ProfanityFilter()

class Species:
    def __init__(self, copy = None):
        self.name = None
        self.description = None
        self.type1 = None
        self.type2 = None
        self.family = None
        self.variety = None
        self.basic_moves = []
        self.learned_moves = []
        self.state_templates = []
        self.generate()
    def generate(self):
        self.type1 = random.choice(adventure.current.types)
        self.type2 = random.choice(adventure.current.types)
        self.family = random.choice(mon_bodies.body_types)
        self.variety = random.choice(self.family.varieties)
        clean = False
        while not clean:
            words = self.type1.nouns + self.type2.nouns + [self.variety]
            w1 = syllable.tokenize(random.choice(words))
            words += self.family.limbs
            w2 = syllable.tokenize(random.choice(words))
            while w1[0] == w2[0]:
                w2 = syllable.tokenize(random.choice(words))
            w1_amt = random.randint(1, len(w1))
            w2_amt = random.randint(1, len(w2))
            word1 = "".join(w1[:w1_amt])
            word2 = "".join(w2[-w2_amt:])
            self.name = (word1+word2).capitalize()
            clean = detect_slurs.is_clean(self.name)
        descriptor = "".join(w1)
        self.description = "The "+ random.choice(self.type1.adjectives)+\
                " " + descriptor + " " +self.variety
        for i in range(12):
            r = random.random()
            if r < 0.4:
                move = generate_atk(self.type1, self.type2) 
                self.learned_moves.append(move)
            elif r < 0.75:
                move = generate_def(self.type1, self.type2) 
                self.learned_moves.append(move)
            else:
                move = generate_fin(self.type1, self.type2) 
                self.learned_moves.append(move)
        self.basic_moves.append(generate_atk(self.type1, self.type2))
        self.basic_moves.append(generate_atk(self.type1, self.type2))
        self.basic_moves.append(generate_def(self.type1, self.type2))
        self.basic_moves.append(generate_def(self.type1, self.type2))
        self.basic_moves.append(generate_fin(self.type1, self.type2))
        for i in range(5): 
            mon_type = random.choice([self.type1, self.type2])
            scale_type = random.choice(mon_states.scale_types)
            adj = random.choice(mon_type.adjectives + mon_type.nouns)
            self.state_templates.append((scale_type, mon_type, adj))

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
