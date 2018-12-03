from kivy.uix.button import Button
from kivy.uix.screenmanager import RiseInTransition
from kivy.core.window import Window

class Btn(Button):
    def __init__(self, **kwargs):
        super(Btn, self).__init__( **kwargs)
        self.name = ''
        self.text = ''
        self.size_hint_y=None
        self.height= Window.height*.12
        self.background_color = (0.83,0.83,0.83,1)


    def on_press(self):
        self.parent.parent.parent.parent.parent.transition = RiseInTransition()
        self.parent.parent.parent.parent.parent.current = self.name


