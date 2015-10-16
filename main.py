from tkinter import Tk
from client import Client
from pkg_resources import resource_filename
import faulthandler
import platform
import sys
import logging
from configparser import ConfigParser

__author__ = 'ToothlessRebel'

config = ConfigParser()
if config.read('config.ini').__len__() < 1:
    raise EnvironmentError

sys.stderr = open('python.log', 'w')
faulthandler.enable(open('python.log', 'w'))
logging.basicConfig(filename='client.log', level=config['CLIENT'].getint('log_level'))

root = Tk()
root.wm_title("Centurion Client")
icon = ''
system = platform.system()

if system == "Windows":
    icon = 'centurion.ico'
elif system == "Linux":
    icon = 'centurion.xbm'
root.wm_iconbitmap(root, resource_filename('resources.images', icon))
client = Client(root)
root.mainloop()
