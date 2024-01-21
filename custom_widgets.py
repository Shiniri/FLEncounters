
from tkinter.ttk import Combobox, Button
from tkinter import Frame, Entry, StringVar, IntVar, Label, Toplevel, Checkbutton


#-----------------------#
#   RIGHT-SIDE WIDGETS  #
#-----------------------#


class FactionSelector(Frame):

    def __init__(self, parent, faction_list):
        super().__init__(parent)

        self.option_var = StringVar()
        self.dropdown = Combobox(self, textvariable=self.option_var, values=faction_list, exportselection=False)
        self.option_var.set("Faction")
        self.dropdown.pack(side="left", padx=2)

        self.entry1_var = StringVar()
        self.entry1 = Entry(self, textvariable=self.entry1_var, width=5, exportselection=False)
        self.entry1_var.set("%")
        self.entry1.pack(side="left", padx=2)

        self.entry2_var = StringVar()
        self.entry2 = Entry(self, textvariable=self.entry2_var, width=5, exportselection=False)
        self.entry2_var.set("INT")
        self.entry2.pack(side="left", padx=2)


class DensityRestrictionSelector(Frame):

    def __init__(self, parent, pilot_list):
        super().__init__(parent)

        self.option_var = StringVar()
        self.dropdown = Combobox(self, textvariable=self.option_var, values=pilot_list, exportselection=False)
        self.option_var.set("Density Restriction")
        self.dropdown.pack(side="left", padx=2)

        self.entry1_var = StringVar()
        self.entry1 = Entry(self, textvariable=self.entry1_var, width=12, exportselection=False)
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
        self.entry = Entry(self, textvariable=self.entry_var, width=5, exportselection=False)
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

        # Setter thingies
        self.relief_time_setter = VariableSelector(self, "Relief time:")
        self.relief_time_setter.pack(side="top", fill="x")
        self.repop_time_setter = VariableSelector(self, "Repop time:")
        self.repop_time_setter.pack(side="top", fill="x")
        self.density_setter = VariableSelector(self, "Density:")
        self.density_setter.pack(side="top", fill="x")

        # Calculate spawn chance
        spawn_chance_var = StringVar()
        self.spawn_chance_label = Label(
            self,
            textvariable=spawn_chance_var,
            font=("Arial, 14")
        )
        spawn_chance_var.set("Spawn Chance: 0.0%")
        self.spawn_chance_label.pack(side="top", fill="x", pady=5)


#-----------------------#
#   LEFT-SIDE WIDGETS   #
#-----------------------#
        

class Min_Max_Setter(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.label = Label(self, text="MIN / MAX:")
        self.label.pack(side="left", padx=2)

        self.entry_min_var = StringVar()
        self.entry_min = Entry(self, textvariable=self.entry_min_var, width=5, exportselection=False)
        self.entry_min_var.set("INT")
        self.entry_min.pack(side="left", padx=2)

        self.entry_max_var = StringVar()
        self.entry_max = Entry(self, textvariable=self.entry_max_var, width=5, exportselection=False)
        self.entry_max_var.set("INT")
        self.entry_max.pack(side="left", padx=2)
        

class Core_Encounter_Specs(Frame):

    def __init__(self, parent, ship_list, job_list, formation_list):
        super().__init__(parent)

        # Ship Class
        self.ship_by_class_var = StringVar()
        self.ship_by_class_dropdown = Combobox(
            self, 
            textvariable=self.ship_by_class_var,
            values=ship_list,
            exportselection=False
        )
        self.ship_by_class_var.set("Ship by class")
        self.ship_by_class_dropdown.pack(side="top", pady=2)

        # Min / Max of what @Milo?
        self.min_max_setter = Min_Max_Setter(self)
        self.min_max_setter.pack(side="top", pady=5)

        # Job override
        self.job_override_var = StringVar()
        self.job_override_dropdown = Combobox(
            self,
            textvariable=self.job_override_var,
            values=job_list,
            exportselection=False
        )
        self.job_override_var.set("Job Override")
        self.job_override_dropdown.pack(side="top", pady=2)

        # Class override
        self.class_override_var = StringVar()
        self.class_override_dropdown = Combobox(
            self,
            textvariable=self.class_override_var,
            values=ship_list,
            exportselection=False
        )
        self.class_override_var.set("Class Override")
        self.class_override_dropdown.pack(side="top", pady=2)

        # Formation
        self.formation_var = StringVar()
        self.formation_dropdown = Combobox(
            self,
            textvariable=self.formation_var,
            values=formation_list,
            exportselection=False
        )
        self.formation_var.set("Formation")
        self.formation_dropdown.pack(side="top", pady=2)

        # Simultanious Creation
        self.simultanious_creation_var = StringVar()
        self.simultanious_creation_dropdown = Combobox(
            self,
            textvariable=self.simultanious_creation_var,
            values=["YES", "NO"],
            exportselection=False
        )
        self.simultanious_creation_var.set("Simultanious Creation")
        self.simultanious_creation_dropdown.pack(side="top", pady=2)

        # Behaviour
        self.behaviour_var = StringVar()
        self.behaviour_combobox = Combobox(
            self, 
            textvariable=self.behaviour_var,
            values=["trade", "wander", "patrol_path"],
            exportselection=False
        )
        self.behaviour_var.set("Behaviour")
        self.behaviour_combobox.pack(side="top", pady=2)

        # Creation Distance
        self.creation_distance_setter = VariableSelector(self, "Creation Distance: ")
        self.creation_distance_setter.pack(side="top", pady=2)

        # Permutation Weight
        self.permutation_weight_setter = VariableSelector(self, "Permutation Weight: ")
        self.permutation_weight_setter.pack(side="top", pady=2)

        # Arrival Types
        self.buttons = []
        self.button_vars = [IntVar() for i in range(8)]
        button_texts = [
            "buzz", "cruise", "object_all", "tradelane",
            "object_capital", "object_station", "object_jump_gate",
            "object_docking_ring"
        ]
        for i, button_text in enumerate(button_texts):
            self.buttons.append(Checkbutton(self, text=button_text, variable=self.button_vars[i]))
            self.buttons[-1].pack(side="top")


class Rename_Popup(Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.rename_entry_var = StringVar()
        self.rename_entry = Entry(self, textvariable=self.rename_entry_var, width=25, exportselection=False)
        self.rename_entry_var.set("New Permutation")
        self.rename_entry.pack(pady=5)

        self.save_button = Button(self, text="Rename")
        self.save_button.pack()