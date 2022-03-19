import mon_types
import move_types
import random
import adventure

names_in_use = set([None])
class Move:
    def __init__(self, name, type1, type2, move_type):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.move_type = move_type
        self.strong_vs = []
        self.resisted_by = []
        self.on_success = None
def noun1_nounmov(type1, type2, movetype):
    name = (random.choice(type1.nouns) + " " 
            + random.choice(movetype.nouns))
    return name
def noun2_nounmov(type1, type2, movetype):
    name = (random.choice(type2.nouns) + " "
            + random.choice(movetype.nouns))
    return name
def noun1_noun2(type1, type2, movetype):
    name = (random.choice(type1.nouns) + " " 
            + random.choice(type2.nouns))
    return name
def noun2_noun1(type2, type1, movetype):
    name = (random.choice(type1.nouns) + " " 
            + random.choice(type2.nouns))
    return name
name_patterns = [
        noun2_nounmov,
        noun1_nounmov,
        noun1_noun2,
        noun2_noun1,
        ]
def movadj_noun1(type1, type2, movetype):
    name = (random.choice(movetype.adjectives) + 
            " "+ random.choice(type1.nouns))
    return name
fin_name_patterns = [
        movadj_noun1,
        ]
def generate_atk(type1, type2, power = 2):
    move_type = random.choice(move_types.atktypes) 
    name = None
    while name in names_in_use:
        pat = random.choice(name_patterns)
        name = pat(type1, type2, move_type)
    names_in_use.add(name)
    atk = Move(name.capitalize(), type1, type2, move_type)
    t1_strong = adventure.current.strong_vs[type1]
    t2_strong = adventure.current.strong_vs[type2]
    strong = list(random.sample(t1_strong+t2_strong,k=power))
    atk.strong_vs = strong
    t1_resist = adventure.current.resisted_by[type1]
    t2_resist = adventure.current.resisted_by[type2]
    resist = 6-power
    if resist < 1:
        resist = 1
    atk.resisted_by = list(random.sample(t1_resist+t2_resist,k=resist))
    return atk

def generate_def(type1, type2, power = 1):
    move_type = random.choice(move_types.deftypes) 
    name = None
    while name in names_in_use:
        pat = random.choice(name_patterns)
        name = pat(type1, type2, move_type)

    defns = Move(name.capitalize(), type1, type2, move_type)
    t1_strong = adventure.current.strong_vs[type1]
    t2_strong = adventure.current.strong_vs[type2]
    strong = list(random.sample(t1_strong+t2_strong,k=power))
    defns.strong_vs = strong
    return defns
def generate_fin(type1, type2, power = 1):
    move_type = random.choice(move_types.fintypes) 
    name = None
    while name in names_in_use:
        pat = random.choice(fin_name_patterns)
        name = pat(type1, type2, move_type)
    fin = Move(name.capitalize(), type1, type2, move_type)
    t1_strong = adventure.current.strong_vs[type1]
    t2_strong = adventure.current.strong_vs[type2]
    strong = list(random.sample(t1_strong+t2_strong,k=power))
    fin.strong_vs = strong
    t1_resist = adventure.current.resisted_by[type1]
    t2_resist = adventure.current.resisted_by[type2]
    resist = 6-power
    if resist < 1:
        resist = 1
    fin.resisted_by = list(random.sample(t1_resist+t2_resist,k=resist))
    return fin


if __name__ == "__main__":
    for i in range(100):
        type1 = random.choice(adventure.current.types)
        type2 = random.choice(adventure.current.types)
        a = generate_atk(type1, type2)
        d = generate_def(type1, type2)
        f = generate_fin(type1, type2)
        print(a.name)
        print(d.name)
        print(f.name)
