import textwrap
from collections import deque 

import settings

MESSAGE_Y = settings.VIEW_HEIGHT

class MessageLog:
    def __init__(self):
        self.messages = deque(maxlen = 6) 
        self.line_length = 80
        self.unread = 0
    def post(self, message): 
        wrapped_msg = textwrap.fill(str(message), self.line_length)
        lines = wrapped_msg.split('\n')
        self.messages.extend(lines)
        self.unread += len(lines)
    def render(self, term):
        with term.location(0, MESSAGE_Y):
            for message in self.messages:
                print(message+term.clear_eol)
        self.read()
    def read(self):
        self.unread = 0

log = MessageLog()

