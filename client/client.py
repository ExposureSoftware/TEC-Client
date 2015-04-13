#!/usr/bin/env python
__author__ = 'ToothlessRebel'
from socket import socket
from queue import Queue
from time import sleep
from threading import Thread
from .clientui import ClientUI
from configparser import ConfigParser

from pprint import pprint


class Client:
    def __init__(self, master):
        self.master = master
        self.queue = Queue()
        self.config = ConfigParser()
        self.connect = True
        if self.config.read('config.ini').__len__() < 1:
            raise EnvironmentError
        self.ui = ClientUI(master, self, self.queue, self.send)
        self.socket = socket()
        self.listener = Thread(target=self.listen)
        self.listener.start()

        self.master.protocol("WM_DELETE_WINDOW", self.stop)

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
            pprint("Socket looped.")
            sleep(0)
            buffer = str(self.socket.recv(4096), encoding='utf8').split("\r\n")
            for line in buffer:
                if line.find('/\/') == -1:
                    self.ui.draw_output(line)
                else:
                    pprint("Unparsed command: " + line)
        pprint("Socket closing.")
        socket.close(self.socket)

    def stop(self):
        # self.master.destroy()
        pprint("Stopping connection.")
        self.connect = False
        pprint(self.listener.join())
        # self.master.destroy()