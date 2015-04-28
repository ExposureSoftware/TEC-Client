__author__ = 'ToothlessRebel'
from tkinter.font import Font
from preferences.preferences import Preferences
import tkinter as tk  # @todo Import only what's needed.
import re
from collections import deque
import html.parser

from pprint import pprint


class ClientUI(tk.Frame):
    def __init__(self, master, client, queue, send_command):
        super(ClientUI, self).__init__()
        self.client = client
        self.queue = queue
        self.send_command = send_command
        self.master = master
        self.interrupt_input = False
        self.input_buffer = deque()

        menu_bar = tk.Menu(master)
        self.menu_file = tk.Menu(menu_bar, tearoff=0)
        self.menu_file.add_command(label="Preferences", command=self.show_preferences)
        self.menu_file.add_command(label="Disconnect", command=self.client.shutdown)
        self.menu_file.add_command(label="Quit", command=self.client.quit)
        menu_bar.add_cascade(label="Client", menu=self.menu_file)
        self.master.config(menu=menu_bar)

        self.master.grid()
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        self.create_widgets()

        # pprint(vars(master))
        self.side_bar = master.children['side_bar']
        self.output_panel = master.children['output']
        italic_font = Font(self.output_panel, self.output_panel.cget("font"))
        italic_font.configure(slant='italic')
        self.output_panel.tag_configure("italic", font=italic_font)

    def parse_output(self, line):
        # Capture SKOOTs
        if line.find('SKOOT') != -1:
            self.parse_skoot(line)
        else:
            line = re.sub(r"</.*?>", "", line)
            pattern = re.compile(r'<font color="(#[0-9a-fA-F]{6})">')
            segments = pattern.split(line)
            tag = None
            self.draw_output("\n")
            for segment in segments:
                if segment.find('#') == 0:
                    self.output_panel.tag_configure(segment, foreground=segment, font=self.output_panel.cget("font"))
                    tag = segment
                else:
                    # Remove when not playing and coding at same time ;)
                    pprint(segment)
                    self.draw_output(segment, tag)

    def parse_skoot(self, skoot):
        pprint(skoot)

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

        output = tk.Text(
            self.master,
            state=tk.DISABLED,
            name="output",
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        scrollbar.config(command=output.yview)
        output.scrollbar = scrollbar
        output.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        input_area = tk.Entry(self.master, name="input")
        input_area.bind("<Return>", self.parse_input)
        input_area.focus()
        input_area.grid(row=1, sticky=tk.W+tk.E, columnspan=2)

        # This is the side bar configuration.
        side_bar = tk.Frame(name="side_bar")
        side_bar.grid(row=0, column=3, rowspan=2, sticky=tk.S+tk.N)

        # The four status bars
        status_area = tk.Canvas(
            side_bar,
            name="status_area",
            width=65,
            height=75,
            bg='black')
        status_area.create_rectangle(5, 5, 15, 75, fill="red", outline="red")
        status_area.create_rectangle(20, 5, 30, 75, fill="yellow", outline="yellow")
        status_area.create_rectangle(35, 5, 45, 75, fill="blue", outline="blue")
        status_area.create_rectangle(50, 5, 60, 75, fill="green", outline="green")
        status_area.pack(side='bottom')

    def parse_input(self, user_input):
        text = user_input.widget.get()
        user_input.widget.delete(0, tk.END)
        if not self.interrupt_input:
            self.send_command(text)
        else:
            self.input_buffer.append(text)
        if self.client.config['UI'].getboolean('echo_input'):
            self.draw_output((text + "\n"), 'italic')
            self.scroll_output()

    def show_preferences(self):
        prefs = Preferences(self.client)
        prefs.grid()