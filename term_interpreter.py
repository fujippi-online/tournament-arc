from core import DIRECTIONS, term

KEY_BINDS = {
        'q' : 'quit',
        'i' : 'inventory',
        'a' : 'interact_local',
        's' : 'inspect_scene',
}

def tag_key(term, key):
    for key_name in list(DIRECTIONS.keys()):
        if key.code == getattr(term, key_name):
            return key_name
        elif key_name == key:
            return key_name
def _get_signal():
    key = term.inkey()
    key_name = None
    if hasattr(key, "name") and key.name:
        key_name = key.name
    if not key_name:
        key_name = tag_key(term, key)
    if key_name in KEY_BINDS:
        return KEY_BINDS[key_name]
    elif key in KEY_BINDS:
        return KEY_BINDS[key]
    elif key_name:
        return key_name
    else:
        return key
class Signal:
    def __init__(self, name):
        self.name = name
def get_signal():
    name = _get_signal()
    return Signal(name)
