#!/usr/bin/env python
__author__ = 'ToothlessRebel'
from socket import socket
from queue import Queue
from time import sleep
from threading import Thread
from .clientui import ClientUI
from configparser import ConfigParser
import logging
import time

from pprint import pprint


class Client:
    def __init__(self, master):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        pprint(self.log.getEffectiveLevel())
        self.log.warning('Starting logger.')
        self.master = master
        self.queue = Queue()
        self.connect = True
        self.config = ConfigParser()
        if self.config.read('config.ini').__len__() < 1:
            raise EnvironmentError
        self.ui = ClientUI(master, self, self.queue, self.send)
        self.socket = socket()
        self.listener = Thread(target=self.listen)
        self.listener.start()
        self.session_log_name = time.strftime("%d.%m.%Y-%H.%M.%S.txt")

        self.master.protocol("WM_DELETE_WINDOW", self.stop)

    def send(self, command):
        total_successful = 0
        while total_successful < command.__len__():
            successful = self.socket.send(bytes(command[total_successful:] + "\r\n", "UTF-8"))
            if successful == 0:
                raise RuntimeError("Unable to send message.")
            total_successful = total_successful + successful

    def log_session(self, text):
        log_dir = self.config['logging']['log_directory']
        log_filename = log_dir + self.session_log_name
        with open(log_filename, 'a+') as game_log:
            game_log.write(text)

    def listen(self):
        socket.connect(self.socket, ("tec.skotos.net", 6730))
        self.send("/\/Connect: na/a!!n/a")
        while self.connect:
            sleep(0)
            buffer = str(self.socket.recv(4096), encoding='utf8').split("\r\n")
            for line in buffer:
                if line.find('/\/') == -1:
                    self.ui.parse_output(line)
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