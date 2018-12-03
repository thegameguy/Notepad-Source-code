from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition, RiseInTransition, WipeTransition
from kivy.storage.dictstore import DictStore
from notes import Notes
from createnew import CreateNew
from note import Note
from kivy.uix.label import Label
import time


__version__ = '1.0'

#ScreenManager
sm = ScreenManager()

#Screens
notes = Notes()
createnew = CreateNew()

sm.add_widget(notes)
sm.add_widget(createnew)


#Navigational Methods
def toCreatenew(touch):
    sm.transition = RiseInTransition()
    sm.current = 'createnew'

def toNotes(touch):
    sm.transition = SlideTransition(direction = 'left')
    sm.current = 'notes'

def toNotesright(touch):
    sm.transition = SlideTransition(direction = 'right')
    sm.current = 'notes'

def clearcreatenewScreen(touch):
    createnew.txt.text = ''

notes.addnotebutton.bind(on_release = toCreatenew)
notes.addnotebutton.bind(on_release = clearcreatenewScreen)
createnew.actionprevious.bind(on_release = toNotesright)

#Methods

#Retreiving data
def data_retrieve(touch = None):
    notes.stack.clear_widgets()
    store = DictStore('store13.dat')


    if len(store.keys()) <= 1:
        pass
    else:
        index_stamp = store['index']['num']
        index_stamp.reverse()
        for x in index_stamp:
            timestamp = x
            notetext = store[x]['note']
            notetime = store[x]['notetime']
            notecolor_dt = store[x]['color']



            #Note
            note = Note(notetext[10:], timestamp)

            #NoteButton
            notebutton = note.button
            notebutton.background_color = notecolor_dt

            notebutton.name = timestamp
            if len(notetext) >= 20:
                notebutton.text = notetext[:20] + '...' + '\n                                               %s' % notetime
            else:
                notebutton.text = notetext + '\n                                                %s' % notetime
            notes.stack.add_widget(notebutton)

            #NoteScreen
            notescreen = note.notescreen
            notescreen.name = timestamp
            notescreen.txt.text = notetext
            notescreen_color = notebutton.background_color
            notescreen_color = list(notescreen_color)
            notescreen.dropdown.main.background_color = notescreen_color
            sm.add_widget(notescreen)



            def delNote(touch):
                #Deleting on Screen
                var = sm.current
                toNotesright(touch)
                #
                #
                #delete notescreen
                for item in sm.children:
                    if item.name == var:
                        sm.remove_widget(item)

                #delete button
                for item in notes.stack.children:
                    if item.name == var:
                        notes.stack.remove_widget(item)

                #Deleting from shelve
                store = DictStore('store13.dat')
                #removing index

                mylist = store['index']['num']
                mylist.remove(var)
                store['index']['num'] = mylist

                #removing df item
                store.delete(var)
            def note_Update(touch):
                curnote = sm.children[0]

                newnotetext = curnote.txt.text

                notecolor_up_dt = curnote.dropdown.main.background_color
                notecolor_up_dt = list(notecolor_up_dt)

                if curnote.txt.text != '':

                    var = sm.current
                    sm.transition = WipeTransition()
                    sm.current = 'notes'

                    store = DictStore('store13.dat')
                    mylist = store['index']['num']
                    mylist.remove(var)
                    store['index']['num'] = mylist

                    #removing df item
                    store.delete(var)
                    #delete notescreen
                    for item in sm.children:
                        if item.name == var:
                            sm.remove_widget(item)

                    #delete button
                    for item in notes.stack.children:
                        if item.name == var:
                            notes.stack.remove_widget(item)


                            #adding new note
                            #working out timestamp
                            timenow = time.asctime(time.localtime(time.time()))
                            timenow = str(timenow)
                            timeraw = timenow[7:19]
                            strip = timeraw.replace(' ', '')
                            timemark = strip.replace(':','')
                            timestamp = timemark
                            notetime = 'On ' + timenow[:10] + ' at ' + timenow[11:19]

                            #StoreData
                            if 'index' in store.keys():
                                card = store['index']['num']
                                card.append(timestamp)
                                store['index']['num'] = card
                            else:
                                store['index'] = {'num': []}
                                card = store['index']['num']
                                card.append(timestamp)
                                store['index']['num'] = card

                            store[timestamp] = {'note': newnotetext,
                                                'notetime': notetime,
                                                'color': notecolor_up_dt}

                            #Note
                            note = Note(newnotetext[10:], timestamp)
                            #NoteButton
                            notebutton = note.button
                            notebutton.background_color = notecolor_up_dt
                            notebutton.name = timestamp
                            if len(newnotetext) > 20:
                                notebutton.text = newnotetext[:20] + '...' + '\n                                               %s' % notetime
                            else:
                                notebutton.text = newnotetext + '\n                                                ' + notetime
                            notes.stack.add_widget(notebutton, len(notes.stack.children))

                            #NoteScreen
                            notescreen = note.notescreen
                            notescreen.name = timestamp
                            notescreen.txt.text = newnotetext
                            notescreen.dropdown.main.background_color = notecolor_up_dt
                            sm.add_widget(notescreen)
                            notescreen.update_button.bind(on_release = note_Update)
                            notescreen.actionprevious.bind(on_release = toNotesright)
                            notescreen.delete_button.bind(on_release = delNote)




            # binding back, delete and update on notescreen
            notescreen.actionprevious.bind(on_release = toNotesright)
            notescreen.delete_button.bind(on_release = delNote)
            notescreen.update_button.bind(on_release = note_Update)

data_retrieve()
notes.close_button.bind(on_release = data_retrieve)

def findNotes(touch):
    if notes.txt.text != '':
        import re

        keyword = notes.txt.text
        matchlist = []
        for x in notes.stack.children:
            key = x.name
            store = DictStore('store13.dat')
            each = store[key]['note']
            matchobj = re.search(keyword.lower(), each.lower())

            if matchobj:
                matchlist.append(key)

        children = []
        for each in notes.stack.children:
            children.append(each.name)

        for x in matchlist:
            children.remove(x)
        purge = children

        for each in purge:
            for item in notes.stack.children:
                if each == item.name:
                    notes.stack.remove_widget(item)
        if len(notes.stack.children) == 0:
            nofound = Label(text = 'No matches were found.',
                            font_size = '20sp',
                            text_size = (300, 300))
            notes.stack.add_widget(nofound)



notes.search_button.bind(on_release = findNotes)



#Adding note
def newNote(touch):
    #newnotetext
    newnotetext = str(createnew.txt.text)
    notecolor_nw = createnew.dropdown.main.background_color
    notecolor_nw = list(notecolor_nw)


    #if screen is not empty
    if newnotetext != '':
        timenow = time.asctime(time.localtime(time.time()))
        timenow = str(timenow)
        timeraw = timenow[7:19]
        strip = timeraw.replace(' ', '')
        timemark = strip.replace(':','')
        timestamp = timemark
        notetime = 'On ' + timenow[:10] + ' at ' + timenow[11:19]

        sm.transition = WipeTransition()
        sm.current = 'notes'

        #StoreData
        store = DictStore('store13.dat')

        if 'index' in store.keys():
            card = store['index']['num']
            card.append(timestamp)
            store['index']['num'] = card
        else:
            store['index'] = {'num': []}
            card = store['index']['num']
            card.append(timestamp)
            store['index']['num'] = card

        store[timestamp] = {'note': newnotetext,
                            'notetime': notetime,
                            'color': notecolor_nw}

        #Newly added Notes
        #notekey
        #newnotetext

        #Note
        note = Note(newnotetext[10:], timestamp)
        #NoteButton
        notebutton = note.button
        notebutton.background_color = notecolor_nw


        notebutton.name = timestamp
        if len(newnotetext) > 20:
            notebutton.text = newnotetext[:20] + '...' + '\n                                               %s' % notetime
        else:
            notebutton.text = newnotetext + '\n                                                ' + notetime
        notes.stack.add_widget(notebutton, len(notes.stack.children))

        #NoteScreen
        notescreen = note.notescreen
        notescreen.name = timestamp
        notescreen.txt.text = newnotetext
        notescreen.actionprevious.bind(on_release = toNotesright)
        notescreen.dropdown.main.background_color = notecolor_nw
        sm.add_widget(notescreen)

        def delNote(touch):
            #Deleting on Screen
            var = sm.current
            toNotesright(touch)
    
            #delete notescreen
            for item in sm.children:
                if item.name == var:
                    sm.remove_widget(item)

            #delete button
            for item in notes.stack.children:
                if item.name == var:
                    notes.stack.remove_widget(item)

            #Deleting from shelve
            store = DictStore('store13.dat')
            #removing index

            mylist = store['index']['num']
            mylist.remove(var)
            store['index']['num'] = mylist

            #removing item
            store.delete(var)


        def note_Update(touch):
            curnote = sm.children[0]
            newnotetext = curnote.txt.text
            notecolor_nw_up = curnote.dropdown.main.background_color
            notecolor_nw_up = list(notecolor_nw_up)

            if curnote.txt.text != '':

                var = sm.current
                sm.transition = WipeTransition()
                sm.current = 'notes'

                store = DictStore('store13.dat')
                mylist = store['index']['num']
                mylist.remove(var)
                store['index']['num'] = mylist

                #removing df item
                store.delete(var)
                #delete notescreen
                for item in sm.children:
                    if item.name == var:
                        sm.remove_widget(item)

                #delete button
                for item in notes.stack.children:
                    if item.name == var:
                        notes.stack.remove_widget(item)
                        
                        #adding new note
                        #working out timestamp
                        timenow = time.asctime(time.localtime(time.time()))
                        timenow = str(timenow)
                        timeraw = timenow[7:19]
                        strip = timeraw.replace(' ', '')
                        timemark = strip.replace(':','')
                        timestamp = timemark
                        notetime = 'On ' + timenow[:10] + ' at ' + timenow[11:19]

                        #StoreData
                        if 'index' in store.keys():
                            card = store['index']['num']
                            card.append(timestamp)
                            store['index']['num'] = card
                        else:
                            store['index'] = {'num': []}
                            card = store['index']['num']
                            card.append(timestamp)
                            store['index']['num'] = card

                        store[timestamp] = {'note': newnotetext,
                                            'notetime': notetime,
                                            'color': notecolor_nw_up}

                        #Note
                        note = Note(newnotetext[10:], timestamp)
                        #NoteButton
                        notebutton = note.button
                        notebutton.background_color = notecolor_nw_up
                        notebutton.name = timestamp
                        if len(newnotetext) > 20:
                            notebutton.text = newnotetext[:20] + '...' + '\n                                               %s' % notetime
                        else:
                            notebutton.text = newnotetext + '\n                                                ' + notetime
                        notes.stack.add_widget(notebutton, len(notes.stack.children))

                        #NoteScreen
                        notescreen = note.notescreen
                        notescreen.name = timestamp
                        notescreen.txt.text = newnotetext
                        notescreen.dropdown.main.background_color = notecolor_nw_up
                        sm.add_widget(notescreen)
                        notescreen.update_button.bind(on_release = note_Update)
                        notescreen.actionprevious.bind(on_release = toNotesright)
                        notescreen.delete_button.bind(on_release = delNote)

        notescreen.delete_button.bind(on_release = delNote)
        notescreen.update_button.bind(on_release = note_Update)

createnew.savebutton.bind(on_release = newNote)

class NotepadPronto(App):
    def build(self):
        return sm

    def on_pause(self):
      # Here you can save data if needed
        return True

    def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
        pass


if __name__ == '__main__':
    NotepadPronto().run()





