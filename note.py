from btn import Btn
from notescreen import NoteScreen


class Note(object):
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp
        self.button = Btn()
        self.notescreen = NoteScreen()