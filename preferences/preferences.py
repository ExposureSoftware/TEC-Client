__author__ = 'ToothlessRebel'
from tkinter import \
    Frame, \
    Toplevel, \
    Checkbutton, \
    BooleanVar, \
    Label, \
    Button
from tkinter.filedialog import askdirectory

from pprint import pprint


class Preferences(Frame):
    def __init__(self, client):
        # Basic setup
        super(Preferences, self).__init__()
        self.client = client

        # Setup the variables used
        self.echo_input = BooleanVar()
        self.logging = BooleanVar()
        self.echo_input.set(self.client.config['UI'].getboolean('echo_input'))
        self.echo_input.trace("w", self.echo_handler)
        self.log_dir = self.client.config['logging']['log_directory']

        # Build the actual window and widgets
        prefs = Toplevel(self)
        prefs.wm_title("Preferences")
        echo_input_label = Label(prefs, text="Echo Input:")
        logging_label = Label(prefs, text='Log to file:')
        echo_checkbox = Checkbutton(prefs, variable=self.echo_input)
        logging_checkbox = Checkbutton(prefs, variable=self.logging)
        logging_button_text = 'Choose file...' if self.log_dir == "" else self.log_dir
        logging_button = Button(prefs, text=logging_button_text, command=self.logging_pick_location)

        # Pack 'em in.
        echo_input_label.grid(row=0, column=0)
        echo_checkbox.grid(row=0, column=1)
        logging_label.grid(row=1, column=0)
        logging_checkbox.grid(row=1, column=1)
        logging_button.grid(row=1, column=2)

    def logging_pick_location(self):
        location = askdirectory(initialdir="%UserProfile%\Documents\\")
        self.client.config['logging']['log_directory'] = location
        self.write_config()

    def echo_handler(self, arg1, arg2, mode):
        self.client.config['UI']['echo_input'] = 'yes' if self.echo_input.get() else 'no'

    def logging_handler(self, arg1, arg2, mode):
        self.client.config['logging']['log_directory'] = 'yes' if self.logging.get else 'no'
        self.write_config()

    def write_config(self, file='config.ini'):
        self.client.config.write(open(file, 'w'))