import random
import pronouncing
import nltk
from menu import LyricInput

nltk_syll = nltk.tokenize.sonority_sequencing.SyllableTokenizer()

line_formats = []
with open("poetry_lines.txt", "r") as f:
    for line in f:
        line_formats.append(line.strip())

def stress_pattern(line):
    words = line.split()
    words = [w.strip() for w in words]
    phones_opts = map(pronouncing.phones_for_word, words)
    phones = []
    for i,j in zip(phones_opts, words):
        if len(i) > 0:
            phones.append(i[0])
        else:
            phones.append(' '.join(nltk_syll.tokenize(j)))
    stresses = map(pronouncing.stresses, phones)
    return ''.join(stresses)

def count_stresses(line):
    stresses = stress_pattern(line)
    num_stresses = 0
    for s in stresses:
        if int(s) > 0:
            num_stresses += 1
    return num_stresses

class EightAlternating:
    def __init__(self, nouns, verbs, adjectives):
        self.nouns = nouns
        self.verbs = verbs
        self.adjectives = adjectives
        self.words = nouns+verbs+adjectives
        self.lines = [self.generate_line()]
        self.total_lines = 4 #total input by player, that is
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
        score = 0
        words = line.split()
        prev_words = self.lines[-1].split()
        if prev_words[-1] in pronouncing.rhymes(words[-1]):
            score += 40
        for w1 in words:
            for w2 in prev_words:
                if w2 in pronouncing.rhymes(w1):
                    score += 10
        prev_start = ""
        for word in words:
            if word in self.words:
                score += 7
            start = word[0]
            if start == prev_start:
                score += 5
            prev_start = start
        syl1 = pronouncing.syllable_count(self.lines[-1])
        syl2 = pronouncing.syllable_count(line)
        syl_diff = abs(syl1-syl2)
        if syl_diff < 2:
            score += 30
        if score > 100:
            score = 100
        return score/self.total_lines

class Villanelle:
    def __init__(self, nouns, verbs, adjectives):
        self.nouns = nouns
        self.verbs = verbs
        self.adjectives = adjectives
        self.words = nouns+verbs+adjectives
        self.refrain1 = self.generate_line()
        self.refrain2 = None
        self.lines = [self.refrain1]
        self.total_lines = 12 #total input by player, that is
        self.evaluation = 0
        self.phase = 1
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
        if len(self.lines) == 2:
            self.refrain2 = line
        self.lines.append(line)
        if len(self.lines) == 3:
            self.lines.append(" - ")
        if len(self.lines) in [6,14]:
            self.lines.append(self.refrain1)
            self.lines.append(" - ")
        if len(self.lines) in [10,18]:
            self.lines.append(self.refrain2)
            self.lines.append(" - ")
        if len(self.lines) == 22:
            self.lines.append(self.refrain1)
            self.lines.append(self.refrain2)
            return self.evaluation
    def evaluate(self, line):
        score = 50 # following the rules is hard
        words = line.split()
        scheme = 0
        if self.lines[-1] == " - ":
            prev_line = self.lines[-2]
        elif len(self.lines) == 1:
            return score/self.total_lines
        else:
            prev_line = self.lines[-1]
            scheme = 1
        prev_words = prev_line.split()
        scheme_rhymes = pronouncing.rhymes(self.lines[scheme].split()[-1])
        met = count_stresses(self.lines[0])
        met_now = pronouncing.syllable_count(line)
        met_diff = abs(met - met_now)
        if met_diff == 0:
            score += 50
        for word in words:
            if word in self.words:
                score += 10
        syl1 = pronouncing.syllable_count(self.lines[-1])
        syl2 = pronouncing.syllable_count(line)
        syl_diff = abs(syl1-syl2)
        if syl_diff < 2:
            score += 10
        if words[-1] in scheme_rhymes:
            score += 30
        for w1 in words:
            for w2 in prev_words:
                if w2 in pronouncing.rhymes(w1):
                    score += 10
        if score > 100:
            score = 100
        return score/self.total_lines
if __name__ == "__main__":
    import control
    from core import term
    import mon_types
    t1 = random.choice(mon_types.types)
    t2 = random.choice(mon_types.types)
    lf = Villanelle(
            t1.nouns+t2.nouns, 
            t1.verbs+t2.verbs, 
            t1.adjectives+t2.adjectives)
    with term.fullscreen(), term.cbreak(), term.hidden_cursor(), term.keypad():
        score = control.takeover(LyricInput(lf))
    for line in lf.lines:
        print(line)
    print(score)
