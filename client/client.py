#!/usr/bin/env python
__author__ = 'ToothlessRebel'
import tkinter as tk
from tkinter.font import Font
from socket import *
from queue import *
from time import *
from threading import *
# import irc
# from pprint import pprint


class ClientUI:
    def __init__(self, master, queue, send_command):
        # super(ClientUI, self).__init__()
        self.queue = queue
        self.send_command = send_command
        menu_bar = tk.Menu(master)
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Preferences", command=self.show_preferences)
        menu_file.add_command(label="Quit", command=master.destroy)
        menu_bar.add_cascade(label="Client", menu=menu_file)
        master.config(menu=menu_bar)
        master.grid()
        self.create_widgets()
        self.output_panel = master.children['output']
        italic_font = Font(self.output_panel, self.output_panel.cget("font"))
        italic_font.configure(slant='italic')
        self.output_panel.tag_configure("italic", font=italic_font)
        while True:
            self.draw_output()
            sleep(0)
        # pprint(self.output_panel)

    # def get_output(self):
    #     buffer = str(self.socket.recv(4096), encoding='utf8').split("\r\n")
    #     pprint(buffer)
    #     for line in buffer:
    #         line.strip()
    #
    #         if line == '':
    #             continue
    #
    #         self.draw_output()

    def draw_output(self):
        while self.queue.qsize():
            try:
                self.output_panel.configure(state="normal")
                self.output_panel.insert(tk.END, (self.queue.get(0) + "\n"))
                self.output_panel.configure(state="disabled")
            except Queue.empty(self.queue):
                pass

    def create_widgets(self):
        output = tk.Text(self, state=tk.DISABLED, name="output")
        output.grid(row=0)

        input_area = tk.Entry(self, name="input")
        input_area.bind("<Return>", self.send_command)
        input_area.focus()
        input_area.grid(row=1, sticky=tk.W+tk.E)

    @staticmethod
    def show_preferences():
        pass

    # def send_command(self, event):
    #     command = event.widget.get()
    #     print("Sending command " + command)
    #     # pprint(vars(event.widget.master.children['output']))
    #     self.socket.send(bytes(command + "\r\n", 'UTF-8'))
    #     if True:
    #         self.queue.put(command)
    #
    #     event.widget.delete(0, tk.END)


class Client:
    def __init__(self, master):
        # super(Client, self).__init__()
        self.master = master
        self.queue = Queue()
        self.ui = ClientUI(master, self.queue, self.send)
        self.socket = socket()
        socket.connect(self.socket, ("tec.skotos.net", 6730))

        self.listener = Thread(target=self.listen)

    def send(self, command):
        self.socket.send(bytes(command, encoding='utf8'))

    def listen(self):
        while True:
            sleep(0)
            buffer = str(self.socket.recv(406), encoding='utf8').split("\r\n")
            for line in buffer:
                self.queue.put(line)


root = tk.Tk()
client = Client(root)
root.mainloop()