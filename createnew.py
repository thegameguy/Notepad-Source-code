from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionItem
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window

Builder.load_string('''
<Text>:
    id: scrlv
    TextInput:
        font_size: '25sp'
        size_hint: 1, None
        height: max( (len(self._lines)+1) * self.line_height, scrlv.height)

''')

class Text(ScrollView):
    pass

class SaveButton(RelativeLayout, ActionItem):
    def __init__(self, **kwargs):
        super(SaveButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = Window.height*.06
        self.width = Window.width*.20
        self.button = Button(background_color = (0,0.75,1,1))
        self.img = Image(source = 'save.png',
                         pos_hint={'center_x': .5, 'center_y': .5},
                         size_hint = (None, None),
                         height = (Window.height*.06)*.90,
                         width = (Window.width*.20)*.30)
        self.add_widget(self.button)
        self.add_widget(self.img)




class mainbutton(RelativeLayout, ActionItem):
    def __init__(self, **kwargs):
        super(mainbutton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = Window.height*.06
        self.width = Window.width*.20
        self.button = Button(background_color = (0.83,0.83,0.83,1))
        self.img = Image(source = 'marker.png',
                         pos_hint={'center_x': .5, 'center_y': .5},
                         size_hint = (None, None),
                         height = (Window.height*.06)*.90,
                         width = (Window.width*.20)*.30)
        self.add_widget(self.button)
        self.add_widget(self.img)



class drop(DropDown):
    def __init__(self, **kwargs):
        super(drop, self).__init__(**kwargs)
        self.btn = Button(background_color = (0.82,0.70,0.87,1), size_hint_y=None, height=Window.height*.06)
        self.btn.bind(on_release=lambda btn: self.select(btn.background_color))
        self.add_widget(self.btn)

        self.btn2 = Button(background_color = (0.68,0.83,0.94,1), size_hint_y=None, height=Window.height*.06)
        self.btn2.bind(on_release=lambda btn2: self.select(btn2.background_color))
        self.add_widget(self.btn2)

        self.btn3 = Button(background_color = (0.63,0.89,0.84,1), size_hint_y=None, height=Window.height*.06)
        self.btn3.bind(on_release=lambda btn3: self.select(btn3.background_color))
        self.add_widget(self.btn3)

        self.btn4 = Button(background_color = (0.97,0.90,0.62,1), size_hint_y=None, height=Window.height*.06)
        self.btn4.bind(on_release=lambda btn4: self.select(btn4.background_color))
        self.add_widget(self.btn4)

        self.btn5 = Button(background_color = (0.92,0.73,0.6,1), size_hint_y=None, height=Window.height*.06)
        self.btn5.bind(on_release=lambda btn5: self.select(btn5.background_color))
        self.add_widget(self.btn5)

        self.btn0 = Button(background_color = (0.83,0.83,0.83,1), size_hint_y=None, height=Window.height*.06)
        self.btn0.bind(on_release=lambda btn0: self.select(btn0.background_color))
        self.add_widget(self.btn0)
        self._main = mainbutton()
        self.main = self._main.button
        self.main.bind(on_release=self.open)
        self.bind(on_select=lambda instance, x: setattr(self.main, 'background_color', x))



class CreateNew(Screen):
    def __init__(self, **kwargs):
        super(CreateNew, self).__init__(**kwargs)
        self.name = 'createnew'
        self.key = 0
        self.stack = StackLayout(cols = 1,
                                 spacing=0,)

        #ActionBar
        self.actionbar = ActionBar(pos_hint={'top':1},
                                   background_color = (0.50,0.50,0.50,1),
                                   height = Window.height*.06,
                                   width = Window.width)
        self.actionview = ActionView()
        self.actionbar.add_widget(self.actionview)
        self.actionprevious = ActionPrevious(with_previous=True,
                                        app_icon = 'mylogo.png',
                                        previous_image = 'arrow.png',
                                        title = '')
        self.actionview.add_widget(self.actionprevious)

        self._savebutton = SaveButton()
        self.savebutton = self._savebutton.button
        self.actionview.add_widget(self._savebutton)
        self.stack.add_widget(self.actionbar)
        self.scroll = Text()
        self.txt = self.scroll.children[0]
        # self.txt = TextInput(size_hint=(1, .92),
        #                  pos_hint={'center_x': .5,'center_y': .46},
        #                      font_size = '35sp')
        self.stack.add_widget(self.scroll)

        self.dropdown = drop()
        self.actionview.add_widget(self.dropdown._main, -1)
        self.add_widget(self.stack)








