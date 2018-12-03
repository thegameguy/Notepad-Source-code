from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

class AddNew(RelativeLayout, ActionItem):
    def __init__(self, **kwargs):
        super(AddNew, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = Window.height*.06
        self.width = Window.width*.20
        self.button = Button(background_color = (0,0.75,1,1))
        self.img = Image(source = 'plus.png',
                         pos_hint={'center_x': .5, 'center_y': .5},
                         size_hint = (None, None),
                         height = (Window.height*.06)*.90,
                         width = (Window.width*.20)*.30)
        self.add_widget(self.button)
        self.add_widget(self.img)




class SearchButton(RelativeLayout, ActionItem):
    def __init__(self, **kwargs):
        super(SearchButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = Window.height*.06
        self.width = Window.width*.20
        self.button = Button(background_color = (0.25,0.41,0.88,1))
        self.img = Image(source = 'searchbar.png',
                         pos_hint={'center_x': .5, 'center_y': .5},
                         size_hint = (None, None),
                         height = (Window.height*.06)*.90,
                         width = (Window.width*.20)*.30)
        self.add_widget(self.button)
        self.add_widget(self.img)


class CloseButton(Button, ActionItem):
    def __init__(self, **kwargs):
        super(CloseButton, self).__init__(**kwargs)
        self.background_color = (1,0,0,1)
        self.font_size = '25sp'
        self.text = '[b]X[/b]'
        self.size_hint = (None, None)
        self.height = Window.height*.06
        self.width = Window.width*.20
        self.markup = True


class Txt(TextInput, ActionItem):

    def __init__(self, **kwargs):
        super(Txt, self).__init__(**kwargs)
        self.size_hint_y = None
        self.size_hint_x = None
        self.height = Window.height*.06
        self.width = Window.width*.30
        self.multiline = False
        self.font_size = '20sp'



class Notes(Screen):
    def __init__(self, **kwargs):
        super(Notes, self).__init__(**kwargs)
        self.name = 'notes'
        self.stackcon = StackLayout(cols = 1,
                                    spacing=0,)

        #Actionbar
        self.actionbar = ActionBar(background_color = (0.50,0.50,0.50,1),
                                   pos_hint={'top':1},
                                   height = Window.height*.06,
                                   width = Window.width)

        self.actionview = ActionView()
        self.actionprevious = ActionPrevious(with_previous=False,
                                        app_icon = 'icon.png',
                                        previous_image = '',
                                        title = '')


        self._addnotebutton = AddNew()
        self.addnotebutton = self._addnotebutton.button
        self.stack = GridLayout(cols = 1,
                               spacing=0,
                               size_hint_y=None)

        self.scroll = ScrollView(size_hint=(1, None),
                                 size=(Window.width, Window.height-50))

        self.txt = Txt(text = '')

        self.close_button = CloseButton()
        self._search = SearchButton()
        self.search_button = self._search.button


        self.stack.bind(minimum_height=self.stack.setter('height'))


        self.actionbar.add_widget(self.actionview)
        self.actionview.add_widget(self.actionprevious)
        self.actionview.add_widget(self.txt)
        self.actionview.add_widget(self._search)
        self.actionview.add_widget(self._addnotebutton)

        self.stackcon.add_widget(self.actionbar)
        self.scroll.add_widget(self.stack)
        self.stackcon.add_widget(self.scroll)
        self.add_widget(self.stackcon)

        self.search_button.bind(on_release = self.hidetextbar)
        self.close_button.bind(on_release = self.showtextbar)

    def hidetextbar(self, touch):
        if self.txt.text != '':
            self.actionview.remove_widget(self.txt)
            self.actionview.remove_widget(self._search)
            self.actionview.add_widget(self.close_button, 1)
    def showtextbar(self, touch):
        self.actionview.add_widget(self.txt, -2)
        self.actionview.add_widget(self._search, -3)
        self.actionview.remove_widget(self.close_button)










