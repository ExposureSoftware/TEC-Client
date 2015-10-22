from tkinter.font import Font
import math
import tkinter as tk  # @todo Import only what's needed.
import re
from collections import deque
import html.parser
from math import floor
from notes import Notes
from preferences.preferences import Preferences
from plugin_manager.plugin_manager import PluginManager

__author__ = 'ToothlessRebel'


class ClientUI(tk.Frame):
    def __init__(self, master, client, queue, send_command):
        super(ClientUI, self).__init__()
        self.client = client
        self.queue = queue
        self.send_command = send_command
        self.master = master
        self.plugin_manager = PluginManager(self.send_command_with_prefs, self.echo)
        self.interrupt_input = False
        self.interrupt_buffer = deque()
        self.input_buffer = []
        self.input_cursor = 0
        self.list_depth = 0
        self.MAP_OFFSET = 60

        menu_bar = tk.Menu(master)
        self.menu_file = tk.Menu(menu_bar, tearoff=0)
        self.menu_file.add_command(label="Preferences", command=self.show_preferences)
        self.menu_file.add_command(label="Disconnect", command=self.client.shutdown)
        self.menu_file.add_command(label="Quit", command=self.client.quit)
        menu_bar.add_cascade(label="Client", menu=self.menu_file)

        self.create_plugin_menu(menu_bar)

        self.master.config(menu=menu_bar)

        self.master.grid()
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        self.status = dict()
        self.create_widgets()

        self.side_bar = master.children['side_bar']
        self.output_panel = master.children['output_frame'].children['output']
        self.output_panel.configure(state="normal")
        self.output_panel.bind('<Key>', lambda e: 'break')
        self.input = master.children['input']
        self.context_menu = master.children['context_menu']

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
                    elif re.search(r'xch_page', segment):
                        pass  # @todo Actually clear the output buffer?
                    elif re.match(r'font', segment):
                        # Handle font changes
                        # So far I know of size and color attributes.
                        color = re.match(r'font color="(#[0-9a-fA-F]{6})"', segment)
                        if color:
                            color = color.group(1)
                            self.output_panel.tag_configure(color, foreground=color,
                                                            font=self.output_panel.cget("font"))
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
                # We're always going to see this with a Zealotry login. The users don't need to know that
                # though so just suppress it.
                if line.find('Either that user does not exist or has a different password.') < 0:
                    self.draw_output(line, None)

    def draw_tabs(self):
        tabs = ""
        for tab in range(1, self.list_depth):
            tabs += "    "
        return tabs

    def parse_skoot(self, skoot):
        skoot_search = re.search('SKOOT (\d+) (.*)', skoot)
        skoot_number = skoot_search.group(1)
        if skoot_number is not None:
            if skoot_number == '6':
                map_update = skoot_search.group(2).split(',')
                map_elements = [map_update[x:x + 5] for x in range(0, len(map_update), 5)]
                self.update_map(map_elements)
            elif skoot_number == '7':
                compass_update = re.split('\W+', skoot_search.group(2))
                self.update_compass(compass_update)
            elif skoot_number == '8':
                status_update = re.split('\W+', skoot_search.group(2))
                self.update_status(status_update)
            elif skoot_number == '10':
                exit_update = skoot_search.group(2).split(',')
                exit_elements = [exit_update[x:x + 4] for x in range(0, len(exit_update), 4)]
                self.update_exits(exit_elements)
            elif skoot_number == '9':
                brightness = math.floor(float(skoot_search.group(2)))
                self.update_lighting(brightness)

    def update_lighting(self, brightness):
        brightness = str('{:x}'.format(brightness))
        rgb = '#' + brightness + brightness + brightness
        self.compass_area.configure(bg=rgb)

    def draw_output(self, text, tags=None):
        self.plugin_manager.pre_process(text, tags)
        self.output_panel.insert(tk.END, text, tags)
        self.scroll_output()
        self.plugin_manager.post_process(text, tags)

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
        game_pane = tk.PanedWindow(self.master, orient=tk.VERTICAL)
        game_pane.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        output_frame = tk.Frame(self.master, name='output_frame')
        output_frame.grid()
        tk.Grid.rowconfigure(output_frame, 0, weight=1)
        tk.Grid.columnconfigure(output_frame, 0, weight=1)

        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

        output = tk.Text(
            output_frame,
            name="output",
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        scrollbar.config(command=output.yview)
        output.scrollbar = scrollbar
        output.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        game_pane.add(output_frame)
        output.bind("<Configure>", self.set_line_length)

        input_area = tk.Text(
            self.master,
            name="input",
            height=1
        )
        input_area.bind("<Return>", self.parse_input)
        input_area.bind("<Up>", self.traverse_up_input_buffer)
        input_area.bind("<Down>", self.traverse_down_input_buffer)
        input_area.focus()
        game_pane.add(input_area)

        # This is the side bar configuration.
        side_bar = tk.Frame(name="side_bar")
        side_bar.grid(row=0, column=3, rowspan=2, sticky=tk.S + tk.N)

        self.create_status_area(side_bar)

        self.create_compass_area(side_bar)
        self.create_map_area(side_bar)
        self.create_macro_area(side_bar)

        # This is the area for plugins
        self.create_plugin_area()

        # Build a context menu for the output pane.
        context_menu = tk.Menu(self.master, tearoff=0, name="context_menu")
        context_menu.add_command(label="Notes", command=self.notes)
        context_menu.add_command(label="Define", state="disabled")

        output.bind("<Button-3>", self.show_context)

    def show_context(self, event):
        selection = ''
        try:
            selection = self.output_panel.get('sel.first', 'sel.last')
        except tk.TclError:
            self.context_menu.entryconfig('Notes', state='disabled')
        if len(selection):
            self.context_menu.entryconfig('Notes', state='normal')
        self.context_menu.post(event.x_root, event.y_root)

    def create_status_area(self, side_bar):
        self.status_area = tk.Canvas(side_bar, name="status_area", width=80, height=105, bg='black')
        self.status_area.bind("<Button-1>", lambda command: self.send_command("condition"))

        self.status_area.create_rectangle(5, 5, 15, 105, fill="#3c0203", outline="#3c0203")
        self.status['health'] = self.status_area.create_rectangle(5, 5, 15, 105, fill="#e30101", outline="#e30101")

        self.status_area.create_rectangle(20, 5, 30, 105, fill="#3d3f04", outline="#3d3f04")
        self.status['fatigue'] = self.status_area.create_rectangle(20, 5, 30, 105, fill="#e2e201", outline="#e2e201")

        self.status_area.create_rectangle(35, 5, 45, 105, fill="#023f3f", outline="#023f3f")
        self.status['encumbrance'] = self.status_area.create_rectangle(35, 5, 45, 105, fill="#00e2e2",
                                                                       outline="#00e2e2")

        self.status_area.create_rectangle(50, 5, 60, 105, fill="#044006", outline="#044006")
        self.status['satiation'] = self.status_area.create_rectangle(50, 5, 60, 105, fill="#00e201", outline="#00e201")
        self.status_area.pack(side='bottom')

    def update_status(self, status_update):
        if status_update and status_update[0]:
            if status_update[0] == 'Health':
                self.status_area.coords(self.status['health'], 5, 105 - int(status_update[1]), 15, 105)
            elif status_update[0] == 'Fatigue':
                self.status_area.coords(self.status['fatigue'], 20, 105 - int(status_update[1]), 30, 105)
            elif status_update[0] == 'Encumbrance':
                self.status_area.coords(self.status['encumbrance'], 35, 105 - int(status_update[1]), 45, 105)
            elif status_update[0] == 'Satiation':
                self.status_area.coords(self.status['satiation'], 50, 105 - int(status_update[1]), 60, 105)

            self.plugin_manager.status_update(status_update[0], status_update[1])

    def create_compass_area(self, side_bar):

        self.compass_area = tk.Canvas(side_bar, name="compass", width=78, height=78, bg='black')

        self.compass = dict()
        self.compass['nw'] = self.compass_area.create_rectangle(5, 5, 25, 25, fill="grey", tags="nw")
        self.compass['n'] = self.compass_area.create_rectangle(30, 5, 50, 25, fill="grey", tags="n")
        self.compass['ne'] = self.compass_area.create_rectangle(55, 5, 75, 25, fill="grey", tags="ne")

        self.compass['w'] = self.compass_area.create_rectangle(5, 30, 25, 50, fill="grey", tags="w")
        self.compass['u'] = self.compass_area.create_polygon([30, 30, 48, 30, 30, 48], fill="grey", tags="u",
                                                             outline='black')
        self.compass['d'] = self.compass_area.create_polygon([50, 32, 50, 50, 32, 50], fill="grey", tags="d",
                                                             outline='black')
        self.compass['e'] = self.compass_area.create_rectangle(55, 30, 75, 50, fill="grey", tags="e")

        self.compass['sw'] = self.compass_area.create_rectangle(5, 55, 25, 75, fill="grey", tags="sw")
        self.compass['s'] = self.compass_area.create_rectangle(30, 55, 50, 75, fill="grey", tags="s")
        self.compass['se'] = self.compass_area.create_rectangle(55, 55, 75, 75, fill="grey", tags="se")

        self.compass_area.pack(side='bottom')

        for key, value in self.compass.items():
            self.compass_area.tag_bind(value, '<ButtonPress-1>',
                                       lambda event, direction=key: self.send_command("go " + direction))

    def update_compass(self, compass_update):
        for i in range(0, 20, 2):
            color = "white" if compass_update[i + 1] == 'show' else 'grey'
            self.compass_area.itemconfigure(self.compass[compass_update[i]], fill=color)

    def update_exits(self, connections):
        for position in connections:
            if len(position) == 4:
                x = int(position[0]) + self.MAP_OFFSET
                y = int(position[1]) + self.MAP_OFFSET
                color = "white" if position[3] == "1" else "black"
                coords = self.compute_exit_line(x, y, position[2])
                self.map_area.create_line(coords[1][0], coords[1][1], coords[1][2], coords[1][3], fill=color, width=2)
                self.map_area.create_line(coords[0][0], coords[0][1], coords[0][2], coords[0][3], fill="black")
                self.map_area.create_line(coords[2][0], coords[2][1], coords[2][2], coords[2][3], fill="black")
            x = int(position[0]) + 60
            y = int(position[1]) + 60
            color = "white" if position[3] == "1" else "black"
            coords = self.compute_exit_line(x, y, position[2])
            self.map_area.create_line(coords[1][0], coords[1][1], coords[1][2], coords[1][3], fill=color, width=4)
            self.map_area.create_line(coords[0][0], coords[0][1], coords[0][2], coords[0][3], fill="black")
            self.map_area.create_line(coords[2][0], coords[2][1], coords[2][2], coords[2][3], fill="black")

    def notes(self):
        Notes(self.output_panel.get('sel.first', 'sel.last'))

    @staticmethod
    # Given an x,y coordinate, compute the black lines and white lines which define an exit in the given direction.
    def compute_exit_line(x, y, direction):
        if direction == "ver":
            return [[x - 1, y + 5, x - 1, y - 5],
                    [x, y + 5, x, y - 5],
                    [x + 1, y + 5, x + 1, y - 5]]
        elif direction == "hor":
            return [[x + 5, y - 1, x - 5, y - 1],
                    [x + 5, y, x - 5, y],
                    [x + 5, y + 1, x - 5, y + 1]]
        elif direction == "ne" or direction == "sw":
            return [[x - 3, y + 4, x + 3, y - 4],
                    [x - 3, y + 3, x + 3, y - 3],
                    [x - 3, y + 1, x + 3, y - 1]]
        elif direction == "nw" or direction == "se":
            return [[x - 3, y - 4, x + 3, y + 4],
                    [x - 3, y - 3, x + 3, y + 3],
                    [x - 3, y - 1, x + 3, y + 1]]

    def update_map(self, map_elements):
        self.map_area.delete("all")
        for position in map_elements:
            if len(position) > 4:
                size = int(position[2])
                x = int(position[0]) + self.MAP_OFFSET
                y = int(position[1]) + self.MAP_OFFSET + size
                self.map_area.create_rectangle(x, y, x + size, y - size, fill=position[3])

    def create_map_area(self, side_bar):
        self.map_area = tk.Canvas(side_bar, name="map", width=120, height=120, bg='black')
        self.map_area.pack(side='bottom')

    def create_macro_area(self, side_bar):

        macros = tk.Frame(side_bar, name="macros", width=120, height=120, bg='black')

        tk.Button(macros, text='I', command=lambda: self.send_command("fe1")).grid(row=0, column=0, sticky='WENS')
        tk.Button(macros, text='II', command=lambda: self.send_command("fe2")).grid(row=0, column=1, sticky='WENS')
        tk.Button(macros, text='III', command=lambda: self.send_command("fe3")).grid(row=0, column=2, sticky='WENS')
        tk.Button(macros, text='IV', command=lambda: self.send_command("fe4")).grid(row=0, column=3, sticky='WENS')
        tk.Button(macros, text='V', command=lambda: self.send_command("fe5")).grid(row=0, column=4, sticky='WENS')

        tk.Button(macros, text='VI', command=lambda: self.send_command("fe6")).grid(row=1, column=0, sticky='WENS')
        tk.Button(macros, text='VII', command=lambda: self.send_command("fe7")).grid(row=1, column=1, sticky='WENS')
        tk.Button(macros, text='VIII', command=lambda: self.send_command("fe8")).grid(row=1, column=2, sticky='WENS')
        tk.Button(macros, text='IX', command=lambda: self.send_command("fe9")).grid(row=1, column=3, sticky='WENS')
        tk.Button(macros, text='X', command=lambda: self.send_command("fe10")).grid(row=1, column=4, sticky='WENS')

        tk.Button(macros, text='XI', command=lambda: self.send_command("fe11")).grid(row=2, column=0, sticky='WENS')
        tk.Button(macros, text='XII', command=lambda: self.send_command("fe12")).grid(row=2, column=1, sticky='WENS')
        tk.Button(macros, text='XIII', command=lambda: self.send_command("fe13")).grid(row=2, column=2, sticky='WENS')
        tk.Button(macros, text='XIV', command=lambda: self.send_command("fe14")).grid(row=2, column=3, sticky='WENS')
        tk.Button(macros, text='XV', command=lambda: self.send_command("fe15")).grid(row=2, column=4, sticky='WENS')

        macros.pack(side='bottom')

    def create_plugin_area(self):
        plugin_bar = tk.Frame(name="plugin_bar")
        plugin_bar.grid(row=0, column=4, rowspan=1, sticky=tk.S + tk.N)
        self.plugin_manager.create_plugin_area(plugin_bar)

    def traverse_up_input_buffer(self, event):
        if self.input_cursor < self.input_buffer.__len__():
            self.input_cursor += 1
            self.set_input()

    def traverse_down_input_buffer(self, event):
        if self.input_cursor > 0:
            self.input_cursor -= 1
            self.set_input()
        else:
            self.input.delete('1.0', tk.END)

    def set_input(self):
        self.input.delete('1.0', tk.END)
        self.input.insert('1.0', self.input_buffer[-self.input_cursor])

    def parse_input(self, user_input):
        text = user_input.widget.get('1.0', 'end-1c')
        self.input_buffer.append(user_input.widget.get('1.0', 'end-1c'))
        user_input.widget.delete('1.0', tk.END)
        self.send_command_with_prefs(text)
        return 'break'

    def send_command_with_prefs(self, text):
        if not self.interrupt_input:
            self.send_command(text)
        else:
            self.interrupt_buffer.append(text)

        if self.client.config['UI'].getboolean('echo_input'):
            self.echo(text)

    def echo(self, text):
        self.draw_output(("\n" + text), 'italic')
        self.scroll_output()

    def show_preferences(self):
        prefs = Preferences(self.client)
        prefs.grid()

    def create_plugin_menu(self, menu_bar):
        size = len(menu_bar.children)
        if size > 1:
            menu_bar.delete("Plugins")
        self.menu_plugins = tk.Menu(menu_bar, tearoff=0)
        self.plugin_checkboxes = dict()
        for plugin in self.plugin_manager.plugins:
            self.plugin_checkboxes[plugin] = tk.BooleanVar(value=self.plugin_manager.plugin_enabled[plugin])
            self.menu_plugins.add_checkbutton(label=plugin, var=self.plugin_checkboxes[plugin],
                                              command=lambda name=plugin: self.toggle_plugin(name,
                                                                                             self.plugin_checkboxes[
                                                                                                 name].get()))
        self.menu_plugins.add_command(label="Refresh", command=lambda mb=menu_bar: self.refresh_plugins(menu_bar))

        menu_bar.add_cascade(label="Plugins", menu=self.menu_plugins)

    def refresh_plugins(self, menu_bar):
        self.plugin_manager.setup()
        self.create_plugin_menu(menu_bar)
        self.create_plugin_area()

    def toggle_plugin(self, name, toggle_on):
        self.plugin_manager.toggle_plugin(name, toggle_on)
        self.create_plugin_area()
