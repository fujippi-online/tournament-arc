class StateScale:
    def __init__(self, name, states, mon_type, scale_type):
        self.name = name
        self.states = tuple(states)
        self.current_state = len(states)
        self.mon_type = mon_type
    def state_descriptor(self):
        return self.states[-self.current_state]
    def do_damage(self, damage):
        self.current_state -= damage 
        if self.current_state < 1:
            self.current_state = 1
    def description(self):
        return (self.name.capitalize() + ": " +
            self.state_descriptor().capitalize())
scale_types = []

class ScaleType:
    def __init__(self, name, states):
        self.name = name
        self.states = states
        scale_types.append(self)


ScaleType("aura",
        ["blinding","shining", "radiant", "glowing", "fading", "extinguished"]
        )
ScaleType("armour",
        ["enchanted","reinforced", "strong", "intact", "damaged", "broken"]
        )
ScaleType("tactics",
        ["inpenetrable","dominant", "powerful", "strong", "effective",
            "predictable"]
        )
ScaleType("faith",
        ["unbreakable","true", "strong", "honest", "being tested", "broken"]
        )
ScaleType("toughness",
        ["wild", "rugged", "strong", "steadfast", "holding on", "exhausted"]
        )
body = ScaleType("body",
        ["fresh","fit", "strong", "healthy", "hurt", "knocked down"]
        )

scale_types.remove(body) #not randomly generated bc you can only have one.

def make_scale(scale_type, mon_type, adjective, length):
    name = adjective + " " + scale_type.name
    states = list(scale_type.states[-length:])
    return StateScale(name, states, mon_type, scale_type)

