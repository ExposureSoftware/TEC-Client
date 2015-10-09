__author__ = 'ToothlessRebel'
from tkinter import Tk
from client import Client
from pkg_resources import resource_filename
import faulthandler

faulthandler.enable(open('crash_log.txt', 'w'))
root = Tk()
root.wm_title("The Eternal City")
#root.wm_iconbitmap(root, resource_filename('resources.images', 'eternal_logo.ico'))
client = Client(root)
root.mainloop()