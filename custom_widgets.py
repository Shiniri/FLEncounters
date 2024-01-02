
from tkinter.ttk import Combobox
from tkinter import Frame, Entry, StringVar, Label


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


class DensityRestrictionSelector(Frame):

    def __init__(self, parent, pilot_list):
        super().__init__(parent)

        self.option_var = StringVar()
        self.dropdown = Combobox(self, textvariable=self.option_var, values=pilot_list)
        self.option_var.set("density restriction")
        self.dropdown.pack(side="left", padx=2)

        self.entry1_var = StringVar()
        self.entry1 = Entry(self, textvariable=self.entry1_var, width=12)
        self.entry1_var.set("INT")
        self.entry1.pack(side="left", padx=2)

       
class VariableSelector(Frame):
    """
        This is a more general class used for three widgets:
            1. Relief time
            2. Repop time
            3. Density
    """
    def __init__(self, parent, label_text):
        super().__init__(parent)

        self.label = Label(self, text=label_text)
        self.label.pack(side="left", padx=2)

        self.entry_var = StringVar()
        self.entry = Entry(self, textvariable=self.entry_var, width=5)
        self.entry_var.set("INT")
        self.entry.pack(side="left", padx=2)


class VariableFrame(Frame):
    """
        This is the frame the three Variable Selectors above
        get packed into. I use an extra frame because otherwise
        there is alignment issues for some reason...
    """
    def __init__(self, parent):
        super().__init__(parent)

        # [...]