from tkinter import Toplevel, Frame, Text, INSERT
from pprint import pprint

__author__ = 'ToothlessRebel'


class Notes(Frame):
    def __init__(self, phrase):
        super(Notes, self).__init__()
        self.file = open('notes.txt', 'r+')
        self.phrase = phrase
        self.delimiter = self.file.readline()

        widow = self.draw_window()
        self.text = widow.children['note']
        self.find_phrase(self.phrase)

    def draw_window(self):
        window = Toplevel(self)
        window.wm_title('Notes on: ' + self.phrase)

        text = Text(window, name="note")
        text.grid(row=0, column=0)

        return window

    def find_phrase(self, phrase):
        for line in self.file:
            if not line.lower().strip() == phrase:
                self.skip_section()
            else:
                for content in self.file:
                    if content == self.delimiter:
                        break
                    self.text.insert(INSERT, content)

    def skip_section(self):
        line = self.file.readline()
        while not line == self.delimiter:
            line = self.file.readline()
