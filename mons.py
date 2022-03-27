import random
import adventure
import mon_species
import mon_states
import menu
import control
import settings
import nltk
import profanityfilter
import message
from move_types import ATK, DEF, FIN

names = []
with open("names.txt") as f:
    for line in f:
        names.append(line.strip())
syllable = nltk.tokenize.sonority_sequencing.SyllableTokenizer()
detect_slurs = profanityfilter.ProfanityFilter()
def mon_name():
    w1 = syllable.tokenize(random.choice(names).lower())
    w2 = syllable.tokenize(random.choice(names).lower())
    max_w1 = min(len(w1), 2)
    max_w2 = min(len(w2), 2)
    w1_amt = 1
    w2_amt = 1
    word1 = "".join(w1[:w1_amt])
    word2 = "".join(w2[-w2_amt:])
    name = (word1+word2).capitalize().replace(" ", "")
    clean = detect_slurs.is_clean(name)
    if clean:
        return name
    else:
        return "".join(w1).capitalize()

# "wow bro is this really what a personality is to you?
# that's fucked up" - you, probably
class Personality:
    def __init__(self):
        self.ko_xp = random.choice([1,2])
        self.ko_trust = random.random() + 0.1
        self.ko_mood = random.random()*2
        self.ko_conf = random.random() + 0.1
        self.victory_trust = random.random() + 0.1
        self.victory_mood = random.random()*2
        self.victory_conf = random.random() + 0.1
        self.participation_xp = random.choice([1,2])
        self.koed_mood_damage = random.random()
        self.koed_trust_damage = random.random()
        self.koed_conf_damage = random.random()
        self.damage_dealt_xp = random.random()*0.2
        self.damage_dealt_conf = random.random()*0.2
        self.damage_dealt_mood = random.random()*0.2
        self.damage_dealt_trust = random.random()*0.2
        self.damage_taken_xp = 0.3 - self.damage_dealt_xp
        self.damage_taken_conf_loss = random.random()*0.1
        self.damage_taken_trust_loss = random.random()*0.1
        self.damage_taken_mood_loss = random.random()*0.1
        self.loss_trust_damage = random.random()
        self.loss_conf_damage = random.random()
        self.loss_mood_damage = random.random()*2
        self.forfeit_trust_loss = random.random()
        self.forfeit_conf_loss = random.random()
        self.forfeit_mood_loss = random.random()*2

class Mon:
    def __init__(self, species):
        self.name = species.name + " " + mon_name()
        self.species = species
        self.type1 = self.species.type1
        self.type2 = self.species.type2
        self.trust = 0
        self.confidence = 0 #self-confidence
        self.mood = 4
        self.level = 5
        self.xp = 5
        self.attacks = []
        self.attack_cap = 4
        self.defences = []
        self.defence_cap = 3
        self.finishers = []
        self.finisher_cap = 2
        self.battle_record = None
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
        self.personality = Personality()
    def revive(self):
        self.can_battle = True
    def handle_battle_result(self):
        if not self.battle_record:
            return
        ps = self.personality
        record = self.battle_record
        self.xp += record.num_kos*ps.ko_xp
        self.mood += record.num_kos*ps.ko_mood
        self.trust += record.num_kos*ps.ko_trust
        self.confidence += record.num_kos*ps.ko_conf
        self.xp += record.damage_dealt*ps.damage_dealt_xp
        self.confidence += record.damage_dealt*ps.damage_dealt_conf
        self.trust += record.damage_dealt*ps.damage_dealt_trust
        self.mood += record.damage_dealt*ps.damage_dealt_mood
        self.xp += record.damage_taken*ps.damage_taken_xp
        self.confidence -= record.damage_taken*ps.damage_taken_conf_loss
        self.trust -= record.damage_taken*ps.damage_taken_trust_loss
        self.mood -= record.damage_taken*ps.damage_taken_mood_loss
        if record.koed:
            self.trust -= ps.koed_trust_damage
            self.confidence -= ps.koed_conf_damage
            self.mood -= ps.koed_mood_damage
        if not record.lost:
            self.trust += ps.victory_trust
            self.confidence += ps.victory_conf
            self.mood += ps.victory_mood
        if record.lost and not record.forfeit:
            self.trust -= ps.loss_trust_damage
            self.confidence -= ps.loss_conf_damage
            self.mood -= ps.loss_mood_damage
        elif record.forfeit:
            self.trust -= ps.forfeit_trust_loss
            self.confidence -= ps.forfeit_conf_loss
            self.mood -= ps.forfeit_mood_loss
        message.log.post(f"trust {self.trust}")
        message.log.post(f"mood {self.mood}")
        message.log.post(f"confidence {self.confidence}")
        if record.participated:
            self.xp += ps.participation_xp
        if self.xp >= 10:
            self.xp -= 10
            self.level_up()
        if self.mood < 0 and self.can_battle:
            menu.msg_box(f"{self.name}: I don't feel up to fighting today.")
            menu.msg_box(f"{self.name} became unable to battle.")
        elif self.confidence < 0:
            menu.msg_box(f"{self.name}: I don't think I can do this anymore.")
            menu.msg_box(f"{self.name}: I'm not good enough.")
            menu.msg_box(f"{self.name} gave up and left the team.")
            self.leave_team()
        elif self.trust < 0:
            menu.msg_box(f"{self.name}: Listen. I'm gonna go my own way.")
            menu.msg_box(f"{self.name}: I've had enough and I think I can do "
                    "better alone.")
            menu.msg_box(f"{self.name} left the team.")
            self.leave_team()
        self.battle_record = None
    def leave_team(self):
        if self in adventure.current.party:
            adventure.current.party.remove(self)
        for map_mon in adventure.current.map_party:
            if map_mon.mon == self:
                adventure.current.map_party.remove(map_mon)
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
                   item_info = info, bg = adventure.current.scene,
                   title = "Learn which technique?")
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
                       [(move.name, move) for move in self.attacks],
                       title="Forget which ability?", 
                       bg = adventure.current.scene)
                    forget = control.takeover(option_menu)
                    self.attacks.remove(forget)
            elif len(self.attacks) >= self.attack_cap:
                self.attacks.remove(random.choice(self.attacks))
            self.attacks.append(move)
        elif move.move_type.action == DEF:
            if self in adventure.current.party:
                if len(self.defences) >= self.defence_cap:
                    option_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-2,
                       [(move.name, move) for move in self.defences],
                       title = "Forget which move?", 
                       bg = adventure.current.scene)
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
