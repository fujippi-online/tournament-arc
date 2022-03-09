body_types = []

class BodyType:
    def __init__(self, name, varieties, limbs):
        self.name = name
        self.varieties = varieties
        self.limbs = limbs
        body_types.append(self)

BodyType("Humanoid",
        ["human", "elf", "fairy", "goblin", "orc", "dwarf"],
        ["head", "chest", "belly", "leg", "arm" "face", "mouth", "eye",
            "finger", "foot", "ankle", "wrist", "elbow"])
BodyType("Feline",
        ["cat", "tiger", "lion", "panther", "leopard", "jaguar"],
        ["head", "back", "belly", "leg", "arm" "face", "mouth", "eye",
            "claws", "paw", "tail", "ears", "whiskers", "teeth"])
BodyType("Canine",
        ["dog", "wolf", "hyena", "fox", "hound", "wolverine"],
        ["head", "back", "tummy", "leg", "arm" "face", "mouth", "eye",
            "claws", "paw", "tail", "ears", "snout", "teeth"])
BodyType("Avian",
        ["raven", "hawk", "pigeon", "parrot", "crow", "magpie", "kingfisher",
            "eagle", "penguin"],
        ["head", "back", "underbelly", "leg", "wing" "eye",
            "claws", "feet", "tail", "legs", "beak"])
BodyType("Cephalapod",
        ["octopus", "squid", "cuttlefish", "nautilus"],
        ["tentacles", "eyes", "head", "mouth", "teeth", "suckers"])
