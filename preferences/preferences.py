__author__ = 'ToothlessRebel'
from tkinter import \
    Frame, \
    Toplevel, \
    Checkbutton, \
    BooleanVar, \
    Label

from pprint import pprint


class Preferences(Frame):
    def __init__(self, client):
        # Basic setup
        super(Preferences, self).__init__()
        self.client = client

        # Setup the variables used
        self.echo_input = BooleanVar()
        self.echo_input.set(self.client.config['UI'].getboolean('echo_input'))
        self.echo_input.trace("w", self.echo_handler)

        # Build the actual window and widgets
        prefs = Toplevel(self)
        prefs.wm_title("Preferences")
        echo_input_label = Label(prefs, text="Echo Input:")
        checkbox = Checkbutton(prefs, variable=self.echo_input)

        # Pack 'em in.
        echo_input_label.grid(row=0, column=0)
        checkbox.grid(row=0, column=1)

    def echo_handler(self, x, y, z):
        self.client.config['UI']['echo_input'] = 'yes' if self.echo_input.get() else 'no'
        self.client.config.write(open('config.ini', 'w'))