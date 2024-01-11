
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

        #   RIGHT / PERMUTATIONS COLUMN     #
        """
            In the future I would like to parse existing encounters here,
            so they can be edited easily, which will require a list of existing
            encounters, which is created from ones already saved.
            (Difference exporting / saving?) For now I will only put a list
            of permutations here, because it's quicker to get a usable tool 
            this way.
        """
        self.permutation_listbox = Listbox(self.right_frame)
        self.permutation_listbox.insert(1, "Default")
        self.permutation_listbox.activate(1)
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