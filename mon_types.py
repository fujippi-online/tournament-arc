types = []
class MonType:
    def __init__(self, name, nouns = None, verbs = None, adjectives = None,
            held_items = None, hats = None):
        if nouns == None: nouns = []
        if verbs == None: verbs = []
        if adjectives == None: adjectives = []
        if held_items == None: held_items = []
        if hats == None: hats = []
        self.name = name
        self.nouns = nouns
        self.verbs = verbs 
        self.adjectives = adjectives
        self.held_items = held_items
        self.hats = hats
        types.append(self)
# hats includes all headwear, I'm not going to call the variable fucking
# HEADWEAR am i. maybe you would. disgusting. glasses are a face  hat.
MonType("Accounting",
        nouns = ["spreadsheet", "account", "bonus", "tax", "cash", "debit",
            "credit", "debt", "interest", "pay", "fraud", "books"],
        adjectives = ["profitable", "efficient", "professional", "reconciled",
            "balanced", "periodic", "final", "net", "gross", "year-end"],
        verbs = ["balance","accrue", "depreciate", "offset", "reconcile", 
            "report"],
        held_items = ["calculator", "abacus", "financial report"],
        hats = ["glasses", "bowler hat"])
MonType("Spicy",
        nouns = ["spice", "flavour", "seasoning", "chilli", "pepper", 
            "capsacin", "wasabi", "habanero", "birds eye", "jalapeno",
            "chipotle", "shishito", "ancho", "zinger"],
        adjectives = ["spicy", "hot", "burning", "numbing", "firey",
            "tingling", "painful", "fragrant", "aromatic","zesty",
            "zippy","herbaceous", "flavoursome", "piquant"],
        verbs = ["burn", "taste", "flavour", "season"],
        held_items = ["big chilli", "ladle", "cookbook", "spicy wing"],
        hats = ["sombrero", "cowboy hat", "chef hat", "chilli earrings"])
MonType("Sinuous",
        nouns = ["rope", "string", "noodle", "spaghetti", "snake", "eel"],
        adjectives = ["curvy","stringy","ropey","floppy", "boneless"],
        verbs = ["bind","slither","constrict","coil","flail"],
        held_items = [],
        hats = [])
MonType("Viscous",
        nouns = ["saliva", "goop", "adhesive", "globule", "dough", "slime",
            "slop"],
        adjectives = ["goopy", "gloopy", "gloppy", "thick", "squidgy",
            "viscous"],
        verbs = ["slime", "stick to", "immerse", "absorb", "coat"],
        held_items = [],
        hats = ["beaker"])
MonType("Civil Servant",
        nouns = ["border", "archive", "park", "ranger", "passport", "document",
            "survey", "statistic", "regulation", "constraints", "meeting"],
        adjectives = ["bureaucratic", "procedural", "regulatory", "official",
            "approved", "denied", "municipal", "budgetary", "public"],
        verbs = ["organise", "assess", "hold", "consult", "deny"],
        held_items = ["clipboard", "id card", "permit"],
        hats = ["thick glasses", "crumpled tie", "frown"])
MonType("Sediment",
        nouns = ["boulder", "rock", "cobble", "pebble", "silt", "clay", "sand",
            "loam"],
        adjectives = ["sandy", "powdery", "friable", "layered"],
        verbs = ["roll", "crush", "grind"],
        held_items = ["shovel"],
        hats = ["hardhat", "beach hat"])
MonType("Revolutionary",
        nouns = ["critic", "criticism", "revolution", "union", "cadre",
            "tenet", "thought", "liberation", "struggle"],
        adjectives = ["red", "revolutionary", "unionized", "proletarian",
            "ideological", "conscious", "counter"],
        verbs = ["defenstrate", "revolt", "revolutionise", "critique",
            "protest", "struggle"],
        held_items = ["book", "banner", "revolutionary thought"],
        hats = ["beret", "star cap"])
MonType("Crime",
        nouns = ["theft", "embezzlement", "murder", "fraud", "arson"],
        adjectives = ["shifty", "untrustworthy", "criminal", "murderous",
            "fraudulent", "illegal", "extra-legal", "semi-legal"],
        verbs = ["embezzle", "steal", "rob", "defraud"],
        held_items = ["gun", "bolt cutters", "knife", "smartphone", 
            "duffel bag"],
        hats = [])
MonType("Boring",
        nouns = ["plain", "normal", "meeting", "finger guns", "agenda",
            "minutes", "waiting", "small talk", "paperwork", "data entry"],
        adjectives = ["pasty", "plain", "inane", "derivative", "boring",
        "repetitive", "samey", "endless", "constant"],
        verbs = ["bore", "detain", "extend", "repeat", "drone"],
        held_items = ["item"],
        hats = ["hat"])
MonType("Academic",
        nouns = ["discourse", "thesis", "dissertation", "classroom", 
        "lecture", "university", "grant", "funding", "publication",
        "theory", "discovery", "research", "result"],
        adjectives = ["dialectical", "peer-reviewed", "evidence-based",
            "non-significant", "post-modern", "theoretical", 
            "interdisciplinary", "groundbreaking"],
        verbs = ["study", "research", "correlate", "lecture", "interpret"],
        held_items = ["chalk", "pen", "coffee"],
        hats = ["glasses"])
MonType("Chonky",
        nouns = ["gravity", "belly", "chonk", "meat", "substance"],
        adjectives = ["rotund", "pot-bellied", "expansive", "hungry", "chonky",
            "thicc", "hearty"],
        verbs = ["scarf", "squish", "sit", "body slam", "fall", "compress",
            "scarf"],
        held_items = ["burger", "dumbell", "hotpot"],
        hats = ["trucker hat", "beanie", "tophat"])
MonType("Ceramic",
        nouns = ["pot", "plate", "idol", "brick", "cup", "vase", "grinder"],
        adjectives = ["terracotta", "porcelain", "glazed", "earthenware"],
        verbs = ["glaze", "fire", "contain"],
        held_items = [],
        hats = ["beret"])
MonType("Gun",
        nouns = ["gun", "musket", "rifle", "bullet", "blunderbuss", "cannon",
            "catapult", "launcher", "sling", "launcher", "sling", "pistol"],
        adjectives = ["shiny", "martial", "antique", "high-calibre", "sniper",
            "bayonet"],
        verbs = ["fire", "shoot", "launch", "bombard"],
        held_items = ["gun", "musket", "rifle", "bullet", "blunderbuss", 
            "pistol"],
        hats = ["beret", "army helmet", "sunglasses"])

MonType("Grammar",
        nouns = ["Noun", "Verb", "Adjective", "Syntax", "Sentence",
            "Construction", "Subject", "Predicate", "Relation"],
        adjectives = ["Ungrammatical", "Grammatical", "Syntactic",
            "inter-sentential", "referential", "complete"],
        verbs = ["correct", "state", "utter", "parse"],
        held_items = [],
        hats = [])
MonType("Jazz",
        nouns = ["bassline", "bebop", "harmony", "melody", "dissonance", 
            "lick"],
        adjectives = ["cool", "free", "modal", "experimental", "reharmonized",
            "emotive", "dragging", "rushing", "swinging"],
        verbs = ["play", "harmonize", "vibe check", "improvize"],
        held_items = [],
        hats = [])
MonType("Flame",
        nouns = ["ember", "flame", "inferno", "heat"],
        adjectives = ["hot", "burning", "firey", "flaming", "flickering",
            "scorching"],
        verbs = ["burn", "light", "heat", "immolate", "torch", "scorch"],
        held_items = [],
        hats = [])
MonType("Tree",
        nouns = ["leaf", "branch", "trunk", "root", "sap", "twig", "bark",
            "hollow", "flower", "berry", "pollen", "seed", "nut"],
        adjectives = ["gnarled", "green", "leafy", "oaken", "blooming",
            "evergreen"],
        verbs = ["grow", "absorb", "entwine", "pollinate"],
        held_items = [],
        hats = ["bucket hat"])
MonType("Bush",
        nouns = ["leaf", "branch", "twig", "flower", "berry", "flower",
            "pollen", "seed", "scrub", "brush", "grass", "flax"],
        adjectives = ["grassy", "overgrown", "natural", "plant-based"],
        verbs = ["grow", "carpet", "entangle", "wind", "sting", "scratch"],
        held_items = [],
        hats = ["beanie"])
