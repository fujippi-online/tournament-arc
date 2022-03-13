import datetime
import menu
import settings
import control
import adventure

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
