import control
import random
import adventure
import settings
import menu
import character
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
        damage += 1
    if state.mon_type in atk.resisted_by:
        damage -= 1
    if defns:
        for def_type in defns.strong_vs:
            if atk.type1 == def_type or atk.type2 == def_type:
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
class TeamBattle:
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
        control.takeover(msgbox)
    def update(self, key):
        self.player_actions = []
        self.opp_actions = []
        action_menu = menu.FloatingMenu(0,settings.VIEW_HEIGHT-1,[
            ("Attack", "atk"),
            ("Defend", "def"),
            ("Finish", "fin"),
            ("Tag-out","tag"),
            ("Forfiet","for"),
            ], bg = self)
        mon = self.current_mon
        for i in range(2):
            action = takeover(action_menu)
            if action == "atk":
                action_menu.remove(("Attack", "atk"))
                options =  list([(move.name, move) for move in mon.attacks])
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                self.player_actions.append(takeover(move_menu))
            elif action == "def":
                action_menu.remove(("Defend", "def"))
                options =  list([(move.name, move) for move in mon.defences])
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                self.player_actions.append(takeover(move_menu))
            elif action == "fin":
                action_menu.remove(("Finish", "fin"))
                options =  list([(move.name, move) for move in mon.finishers])
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT, 
                        options, bg = self)
                self.player_actions.append(takeover(move_menu))
            elif action == "tag":
                action_menu.remove(("Tag-out", "tag"))
                options =  list([(teammate.name, teammate) 
                    for teammate in adventure.current.party 
                    if teammate != self.current_mon and teammate.can_battle])
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1, 
                        options, bg = self)
                self.player_tag = takeover(move_menu)
            elif action == "for":
                self.show_message("You forfeit the battle!")
                for mon in adventure.current.party:
                    mon.morale -= 1
                return "LOSS"
        #OPP decision making (lol)
        tag_options =  list([(teammate.name, teammate) 
            for teammate in adventure.current.party 
            if teammate != self.current_mon and teammate.can_battle])
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
            self.show_message(self.current_mon.name + " taggged out for " +
                    self.player_tag.name)
            self.current_mon = self.player_tag
            self.player_tag = None
        if self.opp_tag:
            self.show_message(self.current_opp.name + " taggged out for " +
                    self.opp_tag.name)
            self.current_mon = self.player_tag
            self.player_tag = None
        # KO swap and victory/loss phase
        if not self.current_mon.can_battle:
            self.show_message(self.current_mon.name + " can no longer battle.")
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
                self.show_message(self.current_mon.name + " taggged out for " +
                        self.player_tag.name)
                self.current_mon = self.player_tag
                self.player_tag = None
        if not self.current_opp.can_battle:
            self.show_message(self.current_opp.name + "can no longer battle.")
            options =  list([teammate for teammate in self.opp 
                if teammate != self.current_opp and teammate.can_battle])
            if len(options) == 0:
                self.show_message("The dust clears, and you are victorious.")
                return "WIN"
            else:
                self.current_opp = random.choice(options)
                self.show_message(self.current_opp.name + " stood up to fight.")

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
        self.show_message(actor.name + " used " + fin_move.name)
        hit_state = None
        for state in defender.states:
            if state.mon_type in fin_move.strong_vs:
                self.show_message(fin_move.name + " pierces " +
                        defender.name + "'s" + state.name + "!")
            elif state.current_state != 1:
                hit_state = state
                break
        if hit_state == None:
            hit_state = defender.body
        else:
            self.show_message(defender.name + "'s " + hit_state.name + 
                    " protects it.")
            return
        damage = calc_damage(defender, fin_move, def_move, hit_state)
        if damage > hit_state.current_state:
            ko_verb = random.choice(fin_move.move_type.verbs)
            self.show_message(actor.name + " " + ko_verb + " " + defender.name)
            defender.can_battle = False
    def do_player_attack(self):
        if not self.current_mon.can_battle:
            return
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
        hit_state = None
        for state in self.current_opp.states:
            if state.current_state != 1:
                hit_state = state
                break
        if hit_state == None:
            hit_state = self.current_opp.body
        damage = calc_damage(self.current_opp, player_atk, opp_def, hit_state)
        self.show_message(self.current_mon.name + " " +
                random.choice(player_atk.move_type.verbs) + " " +
                self.current_opp.name + " with " + player_atk.name+".")
        if damage > 0:
            if opp_def:
                self.show_message(self.current_opp.name + 
                        " tried to defend with " + opp_def.name)
            self.show_message("It's a " +
                    random.choice(damage_descriptors[damage]) + " hit!")
        else:
            self.show_message(self.current_opp + "'s " 
                    + opp_def.name + " "+
                    + random.choice(opp_def.move_type.verbs) +" the attack.") 
        hit_state.do_damage(damage)
        self.show_message(self.current_opp.name+"'s " + hit_state.name + 
                " is " + hit_state.state_descriptor() + ".")
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
        hit_state = None
        for state in self.current_mon.states:
            if state.current_state != 1:
                hit_state = state
                break
        if hit_state == None:
            hit_state = self.current_mon.body
        damage = calc_damage(self.current_mon, opp_atk, player_def, hit_state)
        self.show_message(self.current_opp.name + " " +
                random.choice(opp_atk.move_type.verbs) + " " +
                self.current_mon.name + " with " + opp_atk.name+".")
        if damage > 0:
            if player_def:
                self.show_message(self.current_mon.name + 
                        " tried to defend with " + player_def.name)
            self.show_message("It's a " +
                    random.choice(damage_descriptors[damage]) + " hit!")
        else:
            self.show_message(self.current_mon + "'s " 
                    + player_def.name + " "+
                    + random.choice(player_def.move_type.verbs) +" the attack.") 
        hit_state.do_damage(damage)
        self.show_message(self.current_mon.name+"'s " + hit_state.name + 
                " is " + hit_state.state_descriptor() + ".")
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
        self.message = self.mon.name + ": " +\
                self.team.members[0].mon.name + "! Let's rock!"
        self.team.members.append(self)
    def interact(self, scene):
        scene.show_message("Up for a battle?")
        scene.show_message(self.message)
        mons = list([teammate.mon for teammate in self.team.members])
        takeover(TeamBattle(mons))
        scene.show_message("Nice fighting!")

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
        self.message = self.mon.name + ": " +\
                random.choice(openings)+move.name+"!"
        self.team.members.append(self)
    def interact(self, scene):
        scene.show_message(self.message)

if __name__ == "__main__":
    import mon_species
    import mons
    from core import term
    opponents = []
    for i in range(6):
        opponents.append(mons.Mon(mon_species.Species()))
    battle = TeamBattle(opponents)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        takeover(battle)
