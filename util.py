import functools
from UserList import UserList

#class once:
#    def __init__(self, f):
#        self.func = f
#        self.called = False
#        functools.update_wrapper(self.__call__, f)
#    def __call__(self, *args, **kwargs):
#        if not self.called:
#            self.called = True
#            return self.func(*args, **kwargs)
#        else:
#            return

def once(f):
    @functools.wraps(f)
    def do_once(*args, **kwargs):
        if not hasattr(f, 'called'):
            f.called = True
            return f(*args, **kwargs)
        else:
            pass
    return do_once

class RegisterList(UserList):
    def register(self, item):
        self.data.append(item)
        return item
