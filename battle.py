import control
import random
import adventure
import settings
import menu
import character
import cast
from move_types import ATK, DEF, FIN
from control import takeover
from core import term

VIEW_UPPER = (0,0,settings.BAT_WIDTH, settings.VIEW_HEIGHT//2)
VIEW_LOWER = (0,0+settings.VIEW_HEIGHT//2,
        settings.BAT_WIDTH, settings.VIEW_HEIGHT//2)
VIEW_LEFT = (0,0,settings.BAT_WIDTH//2, settings.VIEW_HEIGHT)
VIEW_RIGHT = (0+settings.BAT_WIDTH//2,0,settings.BAT_WIDTH//2, 
        settings.VIEW_HEIGHT)
def calc_damage(mon, atk, defns, state):
    damage = 2
    if state.mon_type in atk.strong_vs:
        damage += 2
    if state.mon_type in atk.resisted_by:
        damage -= 2
    first_def = True
    if defns:
        for def_type in defns.strong_vs:
            if atk.type1 == def_type or atk.type2 == def_type:
                if first_def:
                    damage -= 2
                    first_def = False
                else:
                    damage -= 1
    if damage > 6:
        damage = 6
    if damage < 0:
        damage = 0
    return damage
damage_descriptors = [
        ("nothing",),
        ("decent",),
        ("strong",),
        ("powerful",),
        ("mighty",),
        ("devastating",),
        ("fearsome",),
        ]
class Battle:
    def __init__(self, opposing_team):
        self.opp = opposing_team
        self.current_opp = opposing_team[0]
        self.current_mon = adventure.current.party[0]
        self.player_actions = []
        self.opp_actions = []
        self.player_tag = None
        self.opp_tag = None
    def show_message(self, lines):
        msgbox = menu.MessageBox(lines, bg = self)
        control.takeover(msgbox, clear = False)
    def update(self, key):
        self.player_actions = []
        self.opp_actions = []
        actions_picked = 0
        action_menu = menu.FloatingMenu(0,settings.VIEW_HEIGHT-1,[
            ("Attack", "atk"),
            ("Defend", "def"),
            ("Finish", "fin"),
            ("Tag-out","tag"),
            ("Forfiet","for"),
            ], bg = self)
        cancel_option = [("Cancel", "x")]
        mon = self.current_mon
        while actions_picked < 2:
            action = takeover(action_menu)
            if action == "atk":
                options =  list([(move.name, move) for move in mon.attacks])
                options += cancel_option
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                move = takeover(move_menu)
                if move != "x":
                    self.player_actions.append(move)
                    actions_picked += 1
                    action_menu.remove(("Attack", "atk"))
            elif action == "def":
                options =  list([(move.name, move) for move in mon.defences])
                options += cancel_option
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                move = takeover(move_menu)
                if move != "x":
                    self.player_actions.append(move)
                    actions_picked += 1
                    action_menu.remove(("Defend", "def"))
            elif action == "fin":
                options =  list([(move.name, move) for move in mon.finishers])
                options += cancel_option
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                move = takeover(move_menu)
                if move != "x":
                    self.player_actions.append(move)
                    actions_picked += 1
                    action_menu.remove(("Finish", "fin"))
            elif action == "tag":
                options =  list([(teammate.name, teammate) 
                    for teammate in adventure.current.party 
                    if teammate != self.current_mon and teammate.can_battle])
                options += cancel_option
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1, 
                        options, bg = self)
                move = takeover(move_menu)
                if move != "x":
                    self.player_tag = takeover(move_menu)
                    actions_picked += 1
                    action_menu.remove(("Tag-out", "tag"))
            elif action == "for":
                options = [
                        ("Forfeit", "yes"),
                        ("Actually, maybe not", "x")
                        ]
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1, 
                        options, bg = self)
                move = takeover(move_menu)
                if move != "x":
                    self.show_message("You forfeit the battle!")
                    for mon in adventure.current.party:
                        mon.morale -= 1
                    return "LOSS"
        #OPP decision making (lol)
        tag_options =  list([mon 
            for mon in self.opp
            if mon != self.current_opp and mon.can_battle])
        if random.random() < 0.05 and len(tag_options) > 0:
            self.opp_actions.append(random.choice(self.current_opp.attacks))
            self.opp_tag = random.choice(tag_options)
        elif self.current_mon.body.current_state <= 2 and random.random()< 0.3:
            self.opp_actions.append(random.choice(self.current_opp.finishers))
            self.opp_actions.append(random.choice(self.current_opp.attacks))
        elif self.current_mon.body.current_state <= 2:
            self.opp_actions.append(random.choice(self.current_opp.defences))
            self.opp_actions.append(random.choice(self.current_opp.finishers))
        else:
            self.opp_actions.append(random.choice(self.current_opp.attacks))
            self.opp_actions.append(random.choice(self.current_opp.defences))
        # ATK/FIN phase
        if self.current_mon.speed >= self.current_opp.speed:
            self.do_player_attack()
            self.do_opp_attack()
            self.do_fin(self.current_mon, self.player_actions,
                    self.current_opp, self.opp_actions)
            self.do_fin(self.current_opp, self.opp_actions,
                    self.current_mon, self.player_actions)
        else:
            self.do_opp_attack()
            self.do_player_attack()
            self.do_fin(self.current_opp, self.opp_actions,
                    self.current_mon, self.player_actions)
            self.do_fin(self.current_mon, self.player_actions,
                    self.current_opp, self.opp_actions)
        # TAG phase
        if self.player_tag:
            self.show_message(f"{self.current_mon.name} taggged out for "
                    f"{self.player_tag.name}")
            self.current_mon = self.player_tag
            self.player_tag = None
        if self.opp_tag:
            self.show_message(f"{self.current_opp.name} taggged out for "
                    f"{self.opp_tag.name}")
            self.current_mon = self.player_tag
            self.player_tag = None
        # KO swap and victory/loss phase
        if not self.current_mon.can_battle:
            self.show_message(f"{self.current_mon.name} can no longer battle.")
            options =  list([(teammate.name, teammate) 
                for teammate in adventure.current.party 
                if teammate != self.current_mon and teammate.can_battle])
            if len(options) == 0:
                self.show_message("The last member fell. You lost the fight.")
                return "LOSS"
            else:
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1, 
                        options, bg = self)
                self.player_tag = takeover(move_menu)
                self.show_message(f"{self.current_mon.name} taggged out for "
                        f"{self.player_tag.name}")
                self.current_mon = self.player_tag
                self.player_tag = None
        if not self.current_opp.can_battle:
            self.show_message(f"{self.current_opp.name} can no longer battle.")
            options =  list([teammate for teammate in self.opp 
                if teammate != self.current_opp and teammate.can_battle])
            if len(options) == 0:
                self.show_message("The dust clears, and you are victorious.")
                return "WIN"
            else:
                self.current_opp = random.choice(options)
                self.show_message(f"{self.current_opp.name} stood up to fight.")
    def do_fin(self, actor, actions, defender, defns):
        if not actor.can_battle:
            return
        def_move = None
        for action in defns:
            if action.move_type.action == DEF:
                def_move = action
        for action in actions:
            if action.move_type.action == ATK:
                def_move = None
        fin_move = None
        for action in actions:
            if action.move_type.action == FIN:
                fin_move = action
        if fin_move == None:
            return
        self.show_message(f"{actor.name} used {fin_move.name}")
        hit_state = None
        for state in defender.states:
            if state.mon_type in fin_move.strong_vs:
                self.show_message(f"{fin_move.name} pierces " 
                    f"{defender.name}'s {state.name}!")
            elif state.current_state != 1:
                hit_state = state
                break
        if hit_state == None:
            hit_state = defender.body
        else:
            self.show_message(f"{defender.name}'s {hit_state.name}"
                    " protects it.")
            return
        damage = calc_damage(defender, fin_move, def_move, hit_state)
        if damage > hit_state.current_state:
            ko_verb = random.choice(fin_move.move_type.verbs)
            self.show_message(f"{actor.name} {ko_verb} {defender.name}")
            defender.can_battle = False
        else:
            self.show_message("The attack is not enough to finish"+
                    defender.name)
    def do_player_attack(self):
        opp_def = None
        for action in self.opp_actions:
            if action.move_type.action == DEF:
                opp_def = action
        player_atk = None
        for action in self.player_actions:
            if action.move_type.action == ATK:
                player_atk = action
        if player_atk == None:
            return
        self.do_attack(self.current_mon, player_atk, self.current_opp, opp_def)
    def do_attack(self, attacker, attack, defender, defence):
        if not attacker.can_battle:
            return
        hit_state = None
        for state in defender.states:
            if state.current_state != 1:
                hit_state = state
                break
        if hit_state == None:
            hit_state = defender.body
        damage = calc_damage(defender, attack, defence, hit_state)
        self.show_message(f"{attacker.name} " 
                f"{random.choice(attack.move_type.verbs)} "
                f"{defender.name} with {attack.name}.")
        if damage > 0:
            if defence:
                self.show_message(f"{defender.name}" 
                        f" tried to defend with {defence.name}.")
            self.show_message("It's a "
                    f"{random.choice(damage_descriptors[damage])} hit!")
            hit_state.do_damage(damage)
            self.show_message(f"{defender.name}'s {hit_state.name} " 
                    f"is {hit_state.state_descriptor()}.")
        elif defence == None:
            self.show_message(f"{defender.name}'s {hit_state.name}"
                    " resisted the attack")
        else:
            self.show_message(f"{defender.name}'s {defence.name} "
                    f"{random.choice(defence.move_type.verbs)} the attack.") 
    def do_opp_attack(self):
        if not self.current_opp.can_battle:
            return
        player_def = None
        for action in self.player_actions:
            if action.move_type.action == DEF:
                player_def = action
        opp_atk = None
        for action in self.opp_actions:
            if action.move_type.action == ATK:
                opp_atk = action
        if opp_atk == None:
            return
        self.do_attack(self.current_opp, opp_atk, self.current_mon, player_def)
    def render(self):
        player_info = [
                self.current_mon.name,
                self.current_mon.species.description,
                self.current_mon.type1.name + " " + self.current_mon.type2.name,
                "",
                self.current_mon.body.description()
        ] + list([state.description() for state in self.current_mon.states])
        menu.draw_textbox(VIEW_LEFT, player_info)
        opp_info = [
                self.current_opp.name,
                self.current_opp.species.description,
                self.current_opp.type1.name + " " + self.current_opp.type2.name,
                "",
                self.current_opp.body.description()
        ] + list([state.description() for state in self.current_opp.states])
        menu.draw_textbox(VIEW_RIGHT, opp_info)

class BattleTeam:
    def __init__(self):
        self.members = []

class BattleLeader(character.Character):
    def __init__(self, x, y, mon, team):
        super().__init__(x, y)
        self.mon = mon
        self.name = self.mon.name
        self.symbol = self.name[0]
        self.color = "red"
        self.team = team
        self.message = (f"{self.mon.name} :" 
                f"{self.team.members[0].mon.name}! Let's rock!")
        self.team.members.append(self)
        self.battled = False
    def interact(self, scene):
        if not self.battled:
            scene.show_message("Up for a battle?")
            ques = menu.FloatingMenu(
                    0, settings.VIEW_HEIGHT -4,
                    [
                        ("Yeah", True),
                        ("Nah", False),
                        ("Yeah, nah.", False)], 
                    bg = scene)
            up_for_it = takeover(ques)
            if up_for_it:
                scene.show_message(self.message)
                mons = list([teammate.mon for teammate in self.team.members])
                result = takeover(Battle(mons))
                if result != "LOSS":
                    scene.show_message("Nice fighting!")
                    self.battled = True
                else:
                    handle_loss(scene)
            else:
                scene.show_message("Maybe another time.")
        else:
            scene.show_message("You're pretty strong!")

def handle_loss(scene):
    revive_scene, revive_position = adventure.current.revive_point
    x,y = revive_position
    for mon in adventure.current.party:
        mon.revive()
        if mon.body.current_state == 1:
            mon.body.current_state = 2
    revive_scene.hero = scene.hero
    revive_scene.hero.x = x
    revive_scene.hero.y = y
    adventure.current.scene = revive_scene
    revive_scene.show_message("You don't remember much after the loss, "
            "but somehow you find yourself back in a familiar place.")

class BattleMember(character.Character):
    def __init__(self, x, y, mon, team):
        super().__init__(x, y)
        self.mon = mon
        self.name = self.mon.name
        self.symbol = self.name[0]
        self.color = "green"
        self.team = team
        openings = ["I'm proud of my ",
                "Can you get past my ",
                "My ultimate technique is ",
                "I've mastered ",
                "My teammates respect me for my "]
        move = random.choice(self.mon.defences+self.mon.attacks+
                self.mon.finishers)
        self.message = (f"{self.mon.name} : {random.choice(openings)}"
            f"{move.name}!")
        self.team.members.append(self)
    def interact(self, scene):
        scene.show_message(self.message)

class Wanderer(character.Character):
    def __init__(self, x, y, mon):
        super().__init__(x, y)
        self.mon = mon
        self.name = self.mon.name
        self.symbol = self.name[0]
        self.color = "orange"
        self.message = f"{self.mon.name}: Let's see what you've got!"
        self.battled = False
    def interact(self, scene):
        if not self.battled:
            scene.show_message("Up for a battle?")
            ques = menu.FloatingMenu(
                    0, settings.VIEW_HEIGHT -4,
                    [
                        ("Yeah", True),
                        ("Nah", False),
                        ("Yeah, nah.", False)], 
                    bg = scene)
            up_for_it = takeover(ques)
            if up_for_it:
                scene.show_message(self.message)
                result = takeover(Battle([self.mon]))
                if result != "LOSS":
                    scene.show_message("Nice fighting!")
                    self.battled = True
                    if len(adventure.current.party) < adventure.party_limit:
                        scene.show_message("How about joining forces?")
                        ques = menu.FloatingMenu(
                                0, settings.VIEW_HEIGHT -4,
                                [
                                    ("Definitely.", True),
                                    ("Hell yeah.", True),
                                    ("I dunno...", False),
                                    ("I'll think about it.", False)], 
                                bg = scene)
                        up_for_it = takeover(ques)
                        if up_for_it:
                            scene.show_message("Right on!")
                            self.mon.body.heal(2)
                            scene.foreground.remove(self)
                            m = cast.PartyMember(self.x, self.y, self.mon)
                            scene.foreground.append(m)
                            adventure.current.map_party.append(m)
                            adventure.current.party.append(self.mon)
                else:
                    handle_loss(scene)
            else:
                scene.show_message("Maybe another time.")
        else:
            pass

if __name__ == "__main__":
    import mon_species
    import mons
    from core import term
    opponents = []
    for i in range(6):
        opponents.append(mons.Mon(mon_species.Species()))
    battle = Battle(opponents)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        takeover(battle)
