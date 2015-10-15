from tkinter import Toplevel, Frame, Text, INSERT
from pprint import pprint

__author__ = 'ToothlessRebel'


# @todo Rework this to store notes as notes/phrase.txt in one file per phrase.
# This would be dependant on the installer creating a writable directory somewhere.
class Notes(Frame):
    def __init__(self, phrase):
        super(Notes, self).__init__()
        self.file = open('notes.txt', 'r+')
        self.phrase = phrase
        self.delimiter = self.file.readline()

        self.draw_window()
        # self.find_phrase(self.phrase)

        self.text.grid()
        self.text = self.children['text']


    def draw_window(self):
        window = Toplevel(self)
        window.wm_title('Notes on: ' + self.phrase)

        text = Text(window, name="text")
        # for line in self.file:
        #     pprint(line)
        #     pprint(self.delimiter)
        #     if line == self.delimiter:
        #         break
        #     text.insert(INSERT, line)
        text.grid(row=0, column=0)

    def find_phrase(self, phrase):
        for line in self.file:
            pprint('test: ' + line)
            if not line.lower().strip() == phrase:
                pprint('Skipping a section')
                self.skip_section()
            else:
                for content in self.file:
                    if content == self.delimiter:
                        break
                    pprint('content: ' + content)
                    self.text.insert(INSERT, content)

    def skip_section(self):
        line = self.file.readline()
        while not line == self.delimiter:
            line = self.file.readline()
