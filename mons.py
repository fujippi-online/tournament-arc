import random
import adventure
import mon_species
import mon_states
import menu
import control
import settings
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
        self.xp = 5
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
        body_type = random.choice((self.type1, self.type2))
        adj = random.choice(body_type.adjectives)
        self.body = mon_states.make_scale(mon_states.body, body_type, adj, 3)
        self.states = []
        def_size = min(self.species.tank // 3, 6) 
        def_type = random.choice((self.type1, self.type2))
        scale_type, mon_type, adj = random.choice(species.state_templates)
        scale = mon_states.make_scale(scale_type, mon_type, adj, def_size)
        self.states.append(scale)
        self.can_battle = True
        self.speed = self.species.speed
        self.tank = self.species.tank
        self.wisdom = self.species.wisdom
        self.power = self.species.power
    def revive(self):
        self.can_battle = True
    def handle_victory(self):
        self.xp += 5
        if self.xp >= 10:
            self.xp = 0
            self.level_up()
    def level_up(self):
        self.level += 1
        index = self.level - 5
        choices = self.species.level_up_sequence[index]
        if self in adventure.current.party:  
           msg = menu.MessageBox(f"{self.name} levelled up to level"
               f" {self.level}!") 
           control.takeover(msg)
           info = []
           for move in choices:
               info.append(
                       [f"{move.move_type.name}: {move.type1.name}"
                       f"/ {move.type2.name}"])
           option_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1,
                   [(move.name, move) for move in choices],
                   item_info = info)
           move = control.takeover(option_menu)
           self.learn_move(move)
        else: 
            move = random.choice(choices)
            self.learn_move(move)
    def learn_move(self, move):
        forget = None
        if move.move_type.action == ATK:
            if self in adventure.current.party:
                if len(self.attacks) >= self.attack_cap:
                    option_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-2,
                       [(move.name, move) for move in self.attacks])
                    forget = control.takeover(option_menu)
                    self.attacks.remove(forget)
            elif len(self.attacks) >= self.attack_cap:
                self.attacks.remove(random.choice(self.attacks))
            self.attacks.append(move)
        elif move.move_type.action == DEF:
            if self in adventure.current.party:
                if len(self.defences) >= self.defence_cap:
                    option_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-2,
                       [(move.name, move) for move in self.defences])
                    forget = control.takeover(option_menu)
                    self.defences.remove(forget)
            elif len(self.defences) >= self.defence_cap:
                self.defences.remove(random.choice(self.defences))
            self.defences.append(move)
        elif move.move_type.action == FIN:
            if self in adventure.current.party:
                if len(self.finishers) >= self.finisher_cap:
                    option_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-2,
                       [(move.name, move) for move in self.finishers])
                    forget = control.takeover(option_menu)
                    self.finishers.remove(forget)
            elif len(self.finishers) >= self.finisher_cap:
                self.finishers.remove(random.choice(self.finishers))
            self.finishers.append(move)
        if self in adventure.current.party:
            if forget:
               msg = menu.MessageBox(f"{self.name} forgot about"
                   f" {forget.name}...") 
               control.takeover(msg)
            msg = menu.MessageBox(f"{self.name} learned"
               f" {move.name}!") 
            control.takeover(msg)
if __name__ == "__main__":
    for i in range(20):
        s = mon_species.Species()
        m = Mon(s)
        print(m.name, m.species.description)
