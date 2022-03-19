import random
import pronouncing
from menu import LyricInput

line_formats = []
with open("poetry_lines.txt", "r") as f:
    for line in f:
        line_formats.append(line.strip())

class EightAlternating:
    def __init__(self, nouns, verbs, adjectives):
        self.nouns = nouns
        self.verbs = verbs
        self.adjectives = adjectives
        self.words = nouns+verbs+adjectives
        self.lines = [self.generate_line()]
        self.evaluation = 0
    def generate_line(self): 
        line_template = random.choice(line_formats)
        line = line_template.format(
            noun1 = random.choice(self.nouns),
            noun2 = random.choice(self.nouns),
            noun3 = random.choice(self.nouns),
            verb1 = random.choice(self.verbs),
            verb2 = random.choice(self.verbs),
            verb3 = random.choice(self.verbs),
            adjective1 = random.choice(self.adjectives),
            adjective2 = random.choice(self.adjectives),
            adjective3 = random.choice(self.adjectives))
        return line
    def add_line(self, line):
        score = self.evaluate(line)
        self.evaluation += score
        self.lines.append(line)
        if len(self.lines) > 7:
            return self.evaluation
        else:
            self.lines.append(self.generate_line())
    def evaluate(self, line):
        return 25

if __name__ == "__main__":
    import control
    from core import term
    import mon_types
    t1 = random.choice(mon_types.types)
    t2 = random.choice(mon_types.types)
    lf = EightAlternating(
            t1.nouns+t2.nouns, 
            t1.verbs+t2.verbs, 
            t1.adjectives+t2.adjectives)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        control.takeover(LyricInput(lf))
    for line in lf.lines:
        print(line)
