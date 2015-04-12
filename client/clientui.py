__author__ = 'ToothlessRebel'
from tkinter.font import Font
from preferences.preferences import Preferences
import tkinter as tk


class ClientUI(tk.Frame):
    def __init__(self, master, queue, send_command):
        super(ClientUI, self).__init__()
        self.queue = queue
        self.send_command = send_command
        self.master = master

        menu_bar = tk.Menu(master)
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Preferences", command=self.show_preferences)
        menu_file.add_command(label="Quit", command=master.destroy)
        menu_bar.add_cascade(label="Client", menu=menu_file)
        self.master.config(menu=menu_bar)

        self.master.grid()
        self.create_widgets()

        self.output_panel = master.children['output']
        italic_font = Font(self.output_panel, self.output_panel.cget("font"))
        italic_font.configure(slant='italic')
        self.output_panel.tag_configure("italic", font=italic_font)

    def draw_output(self, line, tags=None):
        self.output_panel.configure(state="normal")
        self.output_panel.insert(tk.END, (line + "\n"), tags)
        self.output_panel.configure(state="disabled")

    def create_widgets(self):
        output = tk.Text(self.master, state=tk.DISABLED, name="output")
        output.grid(row=0)

        input_area = tk.Entry(self.master, name="input")
        input_area.bind("<Return>", self.parse_input)
        input_area.focus()
        input_area.grid(row=1, sticky=tk.W+tk.E)

    def parse_input(self, user_input):
        text = user_input.widget.get()
        user_input.widget.delete(0, tk.END)
        self.send_command(text)
        if True:
            self.draw_output(text, 'italic')

    def show_preferences(self):
        prefs = Preferences(self.master)
        prefs.grid()