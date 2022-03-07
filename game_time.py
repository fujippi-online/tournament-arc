import datetime
import math
import message
import core

NOON_VISION = 6
NIGHT_VISION = 3


class Calendar:
    current_time = datetime.datetime(600, 4, 1, hour = 7, minute = 30)
    turn_time = datetime.timedelta(seconds = 30)
    weekdays = [
            "Huesday",
            "Treesday",
            "Adornsday",
            "Radday",
            "Sufsday",
            "Yerday",
            "Baptday"
    ]
    def update(self):
        self.current_time = self.current_time + self.turn_time
    def current_day(self):
        return Calendar.weekdays[self.current_time.weekday()]
    def render(self, x, y):
        with core.term.location(x, y):
            print(str(self.current_time.time()), self.current_day())

calendar = Calendar()

class TimeVisionUndercoat:
    def update(self, scene):
        amplitude = float(NOON_VISION - NIGHT_VISION)/2.0
        sun_phase = float(calendar.current_time.hour)/24.0
        base_vision = NIGHT_VISION + amplitude
        adjustment = amplitude*-math.cos(2*math.pi*sun_phase)
        current_vision = base_vision + adjustment
        scene.hero.vision_range = int(current_vision)


