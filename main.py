from tkinter import Tk
from client import Client
from pkg_resources import resource_filename
import faulthandler
import platform
import sys
import logging

__author__ = 'ToothlessRebel'

# Set up problem reporting
sys.stderr = open('python.log', 'w')
faulthandler.enable(open('python.log', 'w'))
logging.basicConfig(filename='client.log', level=logging.DEBUG)

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
