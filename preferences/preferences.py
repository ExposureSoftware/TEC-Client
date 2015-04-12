__author__ = 'ToothlessRebel'
from tkinter import Frame, Toplevel


class Preferences(Frame):
    def __init__(self, master):
        super(Preferences, self).__init__()
        prefs = Toplevel(self)
        prefs.wm_title("Preferences")