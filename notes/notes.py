from tkinter import Toplevel, Frame, Text, END
import string
import sys
from appdirs import AppDirs

__author__ = 'ToothlessRebel'


class Notes(Frame):
    def __init__(self, phrase):
        try:
            if sys.frozen is True:
                dirs = AppDirs('Centurion Client', 'Exposure Software')
                resources_dir = dirs.user_data_dir + '\\resources\\'
            else:
                resources_dir = 'resources\\'
        except AttributeError:
            resources_dir = 'resources\\'

        super(Notes, self).__init__()
        self.phrase = phrase.lower().strip().replace(' ', '_')
        self.filename = resources_dir + "notes\\" + self.phrase + '.txt'
        self.window = self.draw_window()
        self.text = self.window.children['note']
        self.draw_note()

    def draw_window(self):
        window = Toplevel(self)
        title = string.capwords(self.phrase.replace('_', ' '))
        window.wm_title('Notes on: ' + title)
        window.protocol('WM_DELETE_WINDOW', self.save_note)

        text = Text(window, name="note")
        text.grid(row=0, column=0)

        return window

    def draw_note(self):
        file = open(self.filename, 'r')
        self.text.insert('1.0', file.read())
        file.close()

    def save_note(self):
        note_text = self.text.get('1.0', END).strip()
        file = open(self.filename, 'w')
        file.write(note_text)
        file.close()
        self.window.destroy()
