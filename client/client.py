#!/usr/bin/env python
__author__ = 'ToothlessRebel'
import tkinter as tk
from tkinter.font import Font
from pprint import pprint


class Client(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        menu_bar = tk.Menu(master)
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Preferences", command=self.show_preferences)
        menu_file.add_command(label="Quit", command=master.destroy)
        menu_bar.add_cascade(label="Client", menu=menu_file)
        master.config(menu=menu_bar)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        output = tk.Text(self, state=tk.DISABLED, name="output")
        output.grid(row=0)

        input_area = tk.Entry(self, name="input")
        input_area.bind("<Return>", self.send_command)
        input_area.focus()
        input_area.grid(row=1, sticky=tk.W+tk.E)

    @staticmethod
    def send_command(event):
        print("Sending command " + event.widget.get())
        # pprint(vars(event.widget.master.children['output']))

        output = event.widget.master.children['output']
        italic_font = Font(output, output.cget("font"))
        italic_font.configure(slant='italic')
        output.tag_configure("italic", font=italic_font)

        if True:
            output.configure(state='normal')
            output.insert(tk.END, (event.widget.get() + "\n"), ('italic'))
            output.configure(state='disabled')

        event.widget.delete(0, tk.END)

    @staticmethod
    def show_preferences():
        foo = "bar"

root = tk.Tk()
client = Client(master=root)
client.mainloop()