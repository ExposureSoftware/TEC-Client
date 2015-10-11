from tkinter import Tk
from client import Client
from pkg_resources import resource_filename
import faulthandler
import platform

__author__ = 'ToothlessRebel'

faulthandler.enable(open('crash_log.txt', 'w'))
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
