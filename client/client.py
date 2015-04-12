#!/usr/bin/env python
__author__ = 'ToothlessRebel'
import tkinter as tk
from tkinter.font import Font
from socket import socket
from queue import Queue
from time import sleep
from threading import Thread


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


class Client:
    def __init__(self, master):
        self.master = master
        self.queue = Queue()
        self.ui = ClientUI(master, self.queue, self.send)
        self.socket = socket()
        self.listener = Thread(target=self.listen)
        self.listener.start()

    def send(self, command):
        total_successful = 0
        while total_successful < command.__len__():
            successful = self.socket.send(bytes(command[total_successful:] + "\r\n", "UTF-8"))
            if successful == 0:
                raise RuntimeError("Unable to send message.")
            total_successful = total_successful + successful

    def listen(self):
        socket.connect(self.socket, ("tec.skotos.net", 6730))
        while True:
            sleep(0)
            buffer = str(self.socket.recv(4096), encoding='utf8').split("\r\n")
            for line in buffer:
                self.ui.draw_output(line)


class Preferences(tk.Frame):
    def __init__(self, master):
        super(Preferences, self).__init__()
        prefs = tk.Toplevel(self)
        prefs.wm_title("Preferences")