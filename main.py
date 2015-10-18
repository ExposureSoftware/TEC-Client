from tkinter import Tk
from client import Client
from configparser import ConfigParser
from appdirs import AppDirs
import faulthandler
import platform
import sys
import logging

__author__ = 'ToothlessRebel'

try:
    if sys.frozen is True:
        dirs = AppDirs('Centurion Client', 'Exposure Software')
        config_file = dirs.user_config_dir + '\\config.ini'
        log_file_python = dirs.user_log_dir + '\\python.log'
        log_file_client = dirs.user_log_dir + '\\client.log'
        resources_dir = dirs.user_data_dir + '\\resources\\'
    else:
        config_file = 'config.ini'
        log_file_python = 'python.log'
        log_file_client = 'client.log'
        resources_dir = 'resources\\'
except AttributeError:
    config_file = 'config.ini'
    log_file_python = 'python.log'
    log_file_client = 'client.log'
    resources_dir = 'resources\\'

config = ConfigParser()
if config.read(config_file).__len__() < 1:
    raise EnvironmentError

sys.stderr = open(log_file_python, 'w')
faulthandler.enable(open(log_file_python, 'w'))
logging.basicConfig(filename=log_file_client, level=config['CLIENT'].getint('log_level'))

root = Tk()
root.wm_title("Centurion Client")
icon = ''
system = platform.system()

if system == "Windows":
    icon = 'centurion.ico'
elif system == "Linux":
    icon = 'centurion.xbm'

root.wm_iconbitmap(root, resources_dir + 'images\\' + icon)
client = Client(root)
root.mainloop()
