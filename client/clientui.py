__author__ = 'ToothlessRebel'
from tkinter.font import Font
from preferences.preferences import Preferences
import tkinter as tk  # @todo Import only what's needed.
import re
from collections import deque
import html.parser
from math import floor

from pprint import pprint


class ClientUI(tk.Frame):
    def __init__(self, master, client, queue, send_command):
        super(ClientUI, self).__init__()
        self.client = client
        self.queue = queue
        self.send_command = send_command
        self.master = master
        self.interrupt_input = False
        self.interrupt_buffer = deque()
        self.input_buffer = []
        self.input_cursor = 0
        self.list_depth = 0

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
        self.input = master.children['input']

        self.char_width = Font(self.output_panel, self.output_panel.cget("font")).measure('0')
        self.line_length = self.calc_line_length(self.output_panel.cget("width"))
        italic_font = Font(self.output_panel, self.output_panel.cget("font"))
        italic_font.configure(slant='italic')
        self.output_panel.tag_configure("italic", font=italic_font)
        bold_font = Font(self.output_panel, self.output_panel.cget("font"))
        bold_font.configure(weight='bold')
        self.output_panel.tag_configure('bold', font=bold_font)
        self.output_panel.tag_configure("center", justify=tk.CENTER)

    def parse_output(self, line):
        # Capture SKOOTs
        if line.find('SKOOT') != -1:
            self.parse_skoot(line)
        else:
            parser = html.parser.HTMLParser()
            line = parser.unescape(line)
            # Before we nuke the HTML closing tags, decide if we need to un-nest some lists.
            if self.list_depth > 0:
                self.list_depth -= line.count('</ul>')
                # pprint('List depth now lowered to: ' + str(self.list_depth))
            line = re.sub(r"</.*?>", "", line)
            tags = []
            self.draw_output("\n")

            # line is now a string with HTML opening tags.
            # Each tag should delineate segment of the string so that if removed the resulting string
            # would be the output line.

            # It can be a subset of (antiquated) HTML tags:
            # center, font, hr, ul, li, pre, b
            pattern = re.compile(r'<(.*?)>')
            segments = pattern.split(line)
            if segments.__len__() > 1:
                for segment in segments:
                    segment = segment.strip('<>')
                    # Not sure if more Pythonic to do this or a dictionary of functions
                    if re.search(r'thinks aloud:', segment):
                        # Just a thought, print it!
                        self.draw_output('<' + segment + '>', tuple(tags))
                    elif re.match(r'font', segment):
                        # Handle font changes
                        # So far I know of size and color attributes.
                        color = re.match(r'font color="(#[0-9a-fA-F]{6})"', segment)
                        if color:
                            color = color.group(1)
                            self.output_panel.tag_configure(color, foreground=color, font=self.output_panel.cget("font"))
                            tags.append(color)
                        # @todo Handle sizes
                    elif re.match(r'hr', segment):
                        i = 0
                        line = ''
                        while i < self.line_length:
                            line += '-'
                            i += 1
                        self.draw_output(line, 'center')
                    elif re.match(r'pre', segment):
                        # For now, we're just handling this as centered because our font is already fixed width.
                        tags.append('center')
                    elif re.match(r'center', segment):
                        tags.append('center')
                    elif re.match(r'b', segment):
                        tags.append('bold')
                    elif re.match(r'ul', segment):
                        self.list_depth += 1
                        # pprint('List depth now raised to: ' + str(self.list_depth))
                        segment.replace('ul', '')
                        if re.match(r'li', segment):
                            segment = segment.replace('li', self.draw_tabs() + "* ")
                            self.draw_output(segment, tuple(tags))
                    elif re.match(r'li', segment):
                        segment = segment.replace('li', self.draw_tabs() + "* ")
                        self.draw_output(segment, tuple(tags))
                    else:
                        # Not a special segment
                        self.draw_output(segment, tuple(tags))
            else:
                self.draw_output(line, None)

    def draw_tabs(self):
        tabs = ""
        for tab in range(1, self.list_depth):
            tabs += "    "
        return tabs

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

    def set_line_length(self, event):
        width = event.width
        self.line_length = self.calc_line_length(width)

    def calc_line_length(self, width):
        return floor((width / self.char_width) - 10)

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
        output.bind("<Configure>", self.set_line_length)

        input_area = tk.Entry(self.master, name="input")
        input_area.bind("<Return>", self.parse_input)
        input_area.bind("<Up>", self.traverse_up_input_buffer)
        input_area.bind("<Down>", self.traverse_down_input_buffer)
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

    def traverse_up_input_buffer(self, event):
        if self.input_cursor < self.input_buffer.__len__():
            self.input_cursor += 1
            self.set_input()

    def traverse_down_input_buffer(self, event):
        if self.input_cursor > 0:
            self.input_cursor -= 1
            self.set_input()
        else:
            self.input.delete(0, tk.END)

    def set_input(self):
        self.input.delete(0, tk.END)
        self.input.insert(0, self.input_buffer[-self.input_cursor])

    def parse_input(self, user_input):
        text = user_input.widget.get()
        self.input_buffer.append(user_input.widget.get())
        user_input.widget.delete(0, tk.END)
        if not self.interrupt_input:
            self.send_command(text)
        else:
            self.interrupt_buffer.append(text)
        if self.client.config['UI'].getboolean('echo_input'):
            self.draw_output(("\n" + text), 'italic')
            self.scroll_output()

    def show_preferences(self):
        prefs = Preferences(self.client)
        prefs.grid()