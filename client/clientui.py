__author__ = 'ToothlessRebel'
from tkinter.font import Font
from preferences.preferences import Preferences
import tkinter as tk
import re

from pprint import pprint


class ClientUI(tk.Frame):
    def __init__(self, master, client, queue, send_command):
        super(ClientUI, self).__init__()
        self.client = client
        self.queue = queue
        self.send_command = send_command
        self.master = master

        menu_bar = tk.Menu(master)
        self.menu_file = tk.Menu(menu_bar, tearoff=0)
        self.menu_file.add_command(label="Preferences", command=self.show_preferences)
        self.menu_file.add_command(label="Disconnect", command=self.client.shutdown)
        self.menu_file.add_command(label="Quit", command=self.client.quit)
        menu_bar.add_cascade(label="Client", menu=self.menu_file)
        self.master.config(menu=menu_bar)

        self.master.grid()
        self.create_widgets()

        self.output_panel = master.children['output']
        italic_font = Font(self.output_panel, self.output_panel.cget("font"))
        italic_font.configure(slant='italic')
        self.output_panel.tag_configure("italic", font=italic_font)

    def parse_output(self, line):
        pattern = re.compile(r'(\x1bci=\d{1,3},\d{1,3},\d{1,3}\x1b)')
        segments = pattern.split(line)
        tag = None
        self.draw_output("\n")
        for segment in segments:
            if re.match(r'\x1b', segment) is not None:
                pattern = re.compile(r"\d{1,3}.")
                number = "#"
                for value in pattern.findall(segment):
                    hex_value = hex(int(value[0:-1]))[2:]
                    number += "00" if hex_value == "0" else hex_value
                # Now that we have a string representing a hexadecimal, sheesh
                # Let's make a tag for the color!
                # Reusing the tag sets the color for ALL tags of that name!
                self.output_panel.tag_configure(number, foreground=number, font=self.output_panel.cget("font"))
                tag = number
            else:
                self.draw_output(segment, tag)

    def draw_output(self, text, tags=None):
        self.output_panel.configure(state="normal")
        # scroll_position = self.output_panel.scrollbar.get()
        self.output_panel.insert(tk.END, text, tags)
        self.output_panel.configure(state="disabled")
        self.scroll_output()

        # If we're logging the session, we need to handle that
        if self.client.config['logging'].getboolean('log_session'):
            self.client.log_session(text)

    def scroll_output(self):
        self.output_panel.see(tk.END)

    def create_widgets(self):
        scrollbar = tk.Scrollbar(self.master)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

        output = tk.Text(self.master, state=tk.DISABLED, name="output", yscrollcommand=scrollbar.set)
        scrollbar.config(command=output.yview())
        output.scrollbar = scrollbar
        output.grid(row=0)

        input_area = tk.Entry(self.master, name="input")
        input_area.bind("<Return>", self.parse_input)
        input_area.focus()
        input_area.grid(row=1, sticky=tk.W+tk.E)

    def parse_input(self, user_input):
        text = user_input.widget.get()
        user_input.widget.delete(0, tk.END)
        self.send_command(text)
        if self.client.config['UI'].getboolean('echo_input'):
            self.draw_output((text + "\n"), 'italic')
            self.scroll_output()

    def show_preferences(self):
        prefs = Preferences(self.client)
        prefs.grid()