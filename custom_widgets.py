
from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Entry
from tkinter import StringVar


class FactionSelector(Frame):

    def __init__(self, parent, faction_list):
        super().__init__(parent)

        self.option_var = StringVar()
        self.dropdown = Combobox(self, textvariable=self.option_var, values=faction_list)
        self.option_var.set("faction")
        self.dropdown.pack(side="left", padx=2)

        self.entry1_var = StringVar()
        self.entry1 = Entry(self, textvariable=self.entry1_var, width=5)
        self.entry1_var.set("%")
        self.entry1.pack(side="left", padx=2)

        self.entry2_var = StringVar()
        self.entry2 = Entry(self, textvariable=self.entry2_var, width=5)
        self.entry2_var.set("INT")
        self.entry2.pack(side="left", padx=2)

       
