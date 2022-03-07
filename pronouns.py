class Pronouns:
    def __init__(self, they, them, their):
        self.they = they
        self.them = them
        self.their = their

neutral = Pronouns("they", "them", "their")
female = Pronouns("she", "her", "hers")
male = Pronouns("he", "him", "his")
nonperson = Pronouns("it", "it", "its")
