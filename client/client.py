#!/usr/bin/env python
__author__ = 'ToothlessRebel'
import tkinter as tk
from socket import socket
from queue import Queue
from time import sleep
from threading import Thread
from .clientui import ClientUI


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
        self.send("/\/Connect: na/a!!n/a")
        while self.connect:
            sleep(0)
            buffer = str(self.socket.recv(4096), encoding='utf8').split("\r\n")
            for line in buffer:
                if line.find('/\/') == -1:
                    self.ui.draw_output(line)
                else:
                    pprint("Unparsed command: " + line)
