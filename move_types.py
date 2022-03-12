import mon_types

atktypes = []
deftypes = []
fintypes = []
#actions
ATK = 1
DEF = 2
FIN = 3
class MoveType:
    def __init__(self, name, action, nouns = None, verbs = None,
            adjectives = None):
        if nouns == None: nouns = []
        if verbs == None: verbs = []
        if adjectives == None: adjectives = []
        self.action = action
        self.name = name
        self.nouns = nouns
        self.verbs = verbs 
        self.adjectives = adjectives
        if action == ATK:
            atktypes.append(self)
        if action == DEF:
            deftypes.append(self)
        if action == FIN:
            fintypes.append(self)

MoveType("Beam",ATK,
        nouns = ["ray", "beam", "blaster","line","stream","laser"],
        verbs = ["shoots", "blasts"])
MoveType("Strike",ATK,
        nouns = ["strike", "punch", "kick", "bash", "impact", "karate", "MMA",
            "boxing", "kickboxing", "flurry"],
        verbs = ["strikes", "hits", "bashes"])
MoveType("Grapple",ATK,
        nouns = ["throw", "slam", "flip", "grapple", "clinch", "reversal",
            "hold"],
        verbs = ["throws", "slams", "flips"])
MoveType("Magic",ATK,
        nouns = ["curse", "spell", "bolt", "charm", "enchantment", "sorcery",
            "seal"],
        verbs = ["assails"])
MoveType("Sharp",ATK,
        nouns = ["cut", "cutter", "slash", "stab", "thrust", "blade", "point"],
        verbs = ["slices", "dices", "cuts", "pierces", "slashes"])
MoveType("Shield",DEF,
        nouns = ["shield", "bubble", "barrier", "buckler", "membrane", "wall",
            "boundary"],
        verbs = ["protects against", "shields", "deflects", "stops"])
MoveType("Dodge",DEF,
        nouns = ["sidestep", "dodge", "manouver", "backflip", "evasion",
            "acrobatics", "retreat", "duck"],
        verbs = ["dodges", "evades", "retreats from", "avoids"])
MoveType("KO",FIN,
        nouns = ["KO", "finisher", "buster", "haymaker"],
        adjectives = ["knockout", "blackout", "haymaker", "final",
            "ultimate", "conclusive"],
        verbs = ["concludes", "ends", "finishes", "KOs"])
MoveType("Blastoff",FIN,
        nouns = ["launcher", "rocket", "star", ""],
        adjectives = ["stratospheric", "atmospheric", "flying", "rocket",
            "blast-off"],
        verbs = ["concludes", "ends", "finishes", "KOs"])
