import datetime
import menu
import settings
import control
import adventure
import geometry

from character import Character
from game_time import calendar


class Healer(Character):
    color = "purple"
    symbol = "&"
    def interact(self, scene):
        scene.show_message("Take a rest?")
        rest_hours = menu.FloatingMenu(0, settings.VIEW_HEIGHT -10,
                list([(str(i) +" hours", i ) for i in range(10)]), bg = scene,
                title = "Rest?")
        hours = control.takeover(rest_hours)
        one_hour = datetime.timedelta(hours = 1)
        for i in range(hours): 
            calendar.current_time += one_hour
            for mon in adventure.current.party:
                mon.body.heal(1)
                for state in mon.states:
                    state.heal(1)
            scene.render()

class InfoGuy(Character):
    color = "blue"
    symbol = "!"
    def __init__(self, x, y, messages):
        super().__init__(x,y)
        self.messages = message
    def interact(self, scene):
        for message in self.messages:
            scene.show_message(message)

class PartyMember(Character):
    color = "orange"
    symbol = "@"
    blocks = True
    def __init__(self, x, y, mon):
        super().__init__(x,y)
        self.mon = mon
        self.name = mon.name
    def update(self, scene):
        if geometry.distance(self.position, scene.hero.position) > 4:
            self.move_towards(scene, scene.hero.position)
        elif geometry.distance(self.position, scene.hero.position) < 2:
            self.move_away_from(scene, scene.hero.position)
        elif geometry.distance(self.position, scene.hero.position) > 30:
            map_util.reposition_item(scene, scene.camera.rect, self)
            

