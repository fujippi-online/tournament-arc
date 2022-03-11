import control
import random
import adventure
import settings
import menu
import character
from control import takeover
from core import term

VIEW_UPPER = (0,0,settings.BAT_WIDTH, settings.VIEW_HEIGHT//2)
VIEW_LOWER = (0,0+settings.VIEW_HEIGHT//2,
        settings.BAT_WIDTH, settings.VIEW_HEIGHT//2)
VIEW_LEFT = (0,0,settings.BAT_WIDTH//2, settings.VIEW_HEIGHT)
VIEW_RIGHT = (0+settings.BAT_WIDTH//2,0,settings.BAT_WIDTH//2, 
        settings.VIEW_HEIGHT)

class TeamBattle:
    def __init__(self, opposing_team):
        self.opp = opposing_team
        self.current_opp = opposing_team[0]
        self.current_mon = adventure.current.party[0]
        self.player_actions = []
        self.opp_actions = []
        self.player_tag = None
        self.oppp_tag = None
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
                    if teammate != self.current_mon])
                move_menu = menu.FloatingMenu(0, settings.VIEW_HEIGHT-1, 
                        options, bg = self)
                self.player_tag = takeover(move_menu)
            elif action == "for":
                self.show_message("You forfeit the battle!")
                for mon in adventure.current.party:
                    mon.morale -= 1
                return control.DONE
        #OPP decision making (lol)
        self.opp_actions.append(random.choice(self.current_opp.attacks))
        self.opp_actions.append(random.choice(self.current_opp.defences))
        # ATK phase
        if self.current_mon.speed >= self.current_opp.speed:
            self.do_player_attack()
            self.do_opp_attack()
        else:
            self.do_opp_attack()
            self.do_player_attack()
    def do_player_attack(self):
        pass
    def do_opp_attack(self):
        pass
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
