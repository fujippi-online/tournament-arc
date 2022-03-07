import datetime

import control

from core import term

title = """
___                                       _      
 ) _       _ _   _   _ _   _   _  _)_    /_) _ _ 
( (_) (_( ) ) ) (_( ) ) ) )_) ) ) (_    / / ) (_ 
                         (_                      


Sam Whitehead 7DRL 2022


           PRESS ANY KEY YOU LIKE
           TO BEGIN PLAYING THE GAME
""".format(year = datetime.datetime.now().year)
class TitleScreen:
    def __init__(self):
        self.shown = False
    def update(self, key):
        if self.shown:
            return control.DONE
        else:
            self.shown = True
    def render(self):
        with term.location(0,0):
            print(title)
