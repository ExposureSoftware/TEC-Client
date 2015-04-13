__author__ = 'ToothlessRebel'
from tkinter import Frame, Toplevel, Checkbutton, IntVar
from configparser import ConfigParser
from pprint import pprint


class Preferences(Frame):
    def __init__(self, master):
        super(Preferences, self).__init__()
        prefs = Toplevel(self)
        prefs.wm_title("Preferences")

        self.parser = ConfigParser()
        if self.parser.read('config.ini').__len__() < 1:
            raise EnvironmentError
        # master.grid()
        var = IntVar()

        c = Checkbutton(master, text="Expand", variable=var)
        c.pack()