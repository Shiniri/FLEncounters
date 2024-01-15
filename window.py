
#-------------------------------------------------------------------------------#
#   ~ The things yond require doing ~                                           #
#   1. Reduceth the amount of boileth'r'd plates in the list functs             #
#   2. Unifyeth frames things wend into                                         #
#   3. Some variables couldst beest m're descriptive                            #
#   4. Map dropdowns to more descriptive names                                  #
#   5. Allign things more nicely                                                #
#   6. Feature: Open existing Encounters                                        #
#   7. Split Columns into multiple files for ease of access                     #
#-------------------------------------------------------------------------------#

# GUI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Button, Listbox

from custom_widgets import (
    FactionSelector, 
    DensityRestrictionSelector, 
    VariableSelector, VariableFrame,
    Core_Encounter_Specs
)
from permutation_state import Permutation_State

# Parsing
from ini_parser import Ini_Parser
import os

# Other stuff
import itertools

def app_loop():
    """
        Main app loop, prompts user the specify a path to EXE before constructing
        main window.
    """
    def on_select_directory():
        directory_path = filedialog.askdirectory(title="Please provide a Freelancer EXE path.")
        if directory_path:
            root.destroy()
            app = Encounters(directory_path)
            app.mainloop()
        else:
            messagebox.showerror("Error", "No directory selected. The application will close.")
            root.destroy()

    # Root properties
    root = tk.Tk()
    root.title("Select Directory")
    root.geometry("300x100")

    tk.Label(root, text="Please provide a Freelancer EXE path.").pack(pady=10)
    select_button = tk.Button(root, text="Select Directory", command=on_select_directory)
    select_button.pack(pady=10)
    root.mainloop()


class Encounters(tk.Tk):

    def __init__(self, install_directory):
        super().__init__()
        self.install_directory = install_directory
        self.parser = Ini_Parser()
        self.title("Encounters")
        self.geometry("620x420")
        # Handles saving data the user has entered
        self.default_permutation_state = Permutation_State()
        self.permutation_states = [self.default_permutation_state]
        self.current_permutation_state = self.permutation_states[0]

        self.construct_main_window()

    def construct_main_window(self):

        # Create three frames for the three columns
        self.left_frame = ttk.Frame(self)
        self.centre_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        # Place the frames in the window
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.centre_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Configure grid columns to equally share space
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Add headers
        self.encounter_label = ttk.Label(self.left_frame, text="ENCOUNTER", font=("Arial", 14))
        self.encounter_label.pack(pady=10)
        self.system_label = ttk.Label(self.centre_frame, text="SYSTEM", font=("Arial", 14))
        self.system_label.pack(pady=10)
        self.permutation_label = ttk.Label(self.right_frame, text="PERMUTATIONS", font=("Arial", 14))
        self.permutation_label.pack(pady=10)

        # Read data
        self.available_pilots = self.create_list_from_ini_field(
            "pilots_population.ini",
            "nickname"
        )
        self.available_factions = self.create_list_from_ini_field(
            "faction_prop.ini",
            "affiliation"
        )
        self.available_shipclasses = self.create_list_from_ini_field(
            "shipclasses.ini",
            "member"
        )
        self.available_npcclasses = self.create_list_from_ini_field(
            "npcships.ini",
            "npc_class"
        )
        self.available_formations = self.create_list_from_ini_field(
            "formations.ini",
            "nickname"
        )

        #-----------------------#
        #   WIDGETS START HERE  #
        #-----------------------#
        """
            In the future I would like to parse existing encounters here,
            so they can be edited easily, which will require a list of existing
            encounters, which is created from ones already saved.
            (Difference exporting / saving?) For now I will only put a list
            of permutations here, because it's quicker to get a usable tool 
            this way.
        """

        #   RIGHT / PERMUTATIONS COLUMN     #
        
        self.permutation_listbox = Listbox(self.right_frame, selectmode="SINGLE")
        self.permutation_listbox.pack(pady=10)

        self.add_permutation_button = Button(self.right_frame, text="New Permutation")
        self.add_permutation_button.pack(pady=10)
        self.rename_permutation_button = Button(self.right_frame, text="Rename Permutation")
        self.rename_permutation_button.pack(pady=10)
        self.delete_permutation_button = Button(self.right_frame, text="Delete Permutation")
        self.delete_permutation_button.pack(pady=10)

        # The most important button!
        self.create_encounter_button = Button(self.right_frame, text="CREATE ENCOUNTER!", font=("Arial", 14))
        self.create_encounter_button.pack(pady=10)

        #   CENTRE / SYSTEM COLUMN   #

        # Faction Selector
        self.faction_selector = FactionSelector(parent=self.centre_frame, faction_list=self.available_factions)
        self.faction_selector.pack(pady=10)

        # Density Restriction
        self.density_restriction_selector = DensityRestrictionSelector(parent=self.centre_frame, pilot_list=self.available_pilots)
        self.density_restriction_selector.pack(pady=10)

        # Relief time / Repop time / Density
        self.variable_frame = VariableFrame(parent=self.centre_frame)
        self.variable_frame.pack(pady=10)

        #   LEFT / ENCOUNTER COLUMN     #

        # Core Encounter Settings
        self.core_encounter_settings = Core_Encounter_Specs(
            parent=self.left_frame,
            ship_list=self.available_shipclasses,
            job_list=self.available_pilots,
            formation_list=self.available_formations
        )
        self.core_encounter_settings.pack(pady=10)

        #   Callback binds  #

        # Permutation Selector
        def _get_and_set_permutation_index(permutation_name):
            for permutation in self.permutation_states:
                if permutation.name == permutation_name:
                    self.current_permutation_state = permutation
                    return permutation
                # TODO: Some error handling?

        def _update_window_by_permutation(permutation):
            # Dropdowns 
            self.core_encounter_settings.ship_by_class_dropdown.set(permutation.ship_by_class)
            self.core_encounter_settings.job_override_dropdown.set(permutation.job_override)
            self.core_encounter_settings.class_override_dropdown.set(permutation.class_override)
            self.core_encounter_settings.formation_dropdown.set(permutation.formation)
            self.core_encounter_settings.simultanious_creation_dropdown.set(permutation.simultanious_creation)
            self.core_encounter_settings.behaviour_combobox.set(permutation.behaviour)
            
            self.faction_selector.dropdown.set(permutation.faction[0])
            self.density_restriction_selector.dropdown.set(permutation.density_restriction[0])

            # INT fields
            self.core_encounter_settings.min_max_setter.entry_max_var.set(self.current_permutation_state.min_max[0])
            self.core_encounter_settings.min_max_setter.entry_min_var.set(self.current_permutation_state.min_max[1])
            self.core_encounter_settings.creation_distance_setter.entry_var.set(self.current_permutation_state.creation_distance)
            self.core_encounter_settings.permutation_weight_setter.entry_var.set(self.current_permutation_state.permutation_weight)
            
            self.faction_selector.entry1_var.set(self.current_permutation_state.faction[1])
            self.faction_selector.entry2_var.set(self.current_permutation_state.faction[2])
            self.density_restriction_selector.entry1_var.set(self.current_permutation_state.density_restriction[1])
            self.variable_frame.relief_time_setter.entry_var.set(self.current_permutation_state.relief)
            self.variable_frame.repop_time_setter.entry_var.set(self.current_permutation_state.repop)
            self.variable_frame.density_setter.entry_var.set(self.current_permutation_state.density)

        def _listbox_callback(event):
            permutation_name = event.widget.get(event.widget.curselection()[0])
            _update_window_by_permutation(_get_and_set_permutation_index(permutation_name))
                
        # <<ListboxSelect>> event does not fucking work. It does weird things
        # and crashes. I don't want to deal with it, thusly:
        self.permutation_listbox.bind(
            "<FocusIn>",
            _listbox_callback
        )

        # Dropdowns
        self.core_encounter_settings.ship_by_class_dropdown.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_ship_select
        )
        self.core_encounter_settings.job_override_dropdown.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_job_override_select
        )
        self.core_encounter_settings.class_override_dropdown.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_class_override_select
        )
        self.core_encounter_settings.formation_dropdown.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_formation_select
        )
        self.core_encounter_settings.simultanious_creation_dropdown.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_simultanious_creation_select
        )
        self.core_encounter_settings.behaviour_combobox.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_behaviour_select
        )
        self.faction_selector.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_faction_select
        )
        self.density_restriction_selector.bind(
            "<<ComboboxSelected>>",
            self.current_permutation_state.on_density_restriction_select
        )

        # This has to be done because otherwise the default values won't spawn
        self.permutation_listbox.insert(0, "Default")
        self.permutation_listbox.selection_set(0)
        self.permutation_listbox.focus_set()
        self.permutation_listbox.event_generate("<FocusIn>")

    def create_list_from_ini_field(self, filename, field_name):

        target_path = self.install_directory + "/DATA/MISSIONS/" + filename
        ini_file = self.parser.read(target_path)

        # Check if file is actually there
        # (parser fails silently / outputs [])
        if ini_file == []:
            messagebox.showerror("Error", f"Failed to find {filename} at specified location.")
            self.destroy

        # Return unique values for field
        values = [block[field_name] for block in ini_file if field_name in block]
        return list(set(list(itertools.chain.from_iterable(values))))