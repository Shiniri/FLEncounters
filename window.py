# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from custom_widgets import FactionSelector

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
        self.geometry("600x400")
        self.construct_main_window()


    def construct_main_window(self):
        # Create two frames for the two columns
        self.left_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        # Place the frames in the window
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Configure grid columns to equally share space
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add headers
        self.encounter_label = ttk.Label(self.left_frame, text="ENCOUNTER", font=("Arial", 14))
        self.system_label = ttk.Label(self.right_frame, text="SYSTEM", font=("Arial", 14))
        self.encounter_label.pack(pady=10)
        self.system_label.pack(pady=10)

        # Read data & populate window accordingly
        self.available_pilots = self.create_pilot_list()
        self.available_factions = self.create_faction_list()
        self.available_shipclasses = self.create_shipclass_list()
        self.available_npcclasses = self.create_npcclass_list()

        # Faction Selector
        self.faction_selector = FactionSelector(parent=self.right_frame, faction_list=self.available_factions)
        self.faction_selector.pack(pady=10)


    def create_pilot_list(self):

        pilot_path = self.install_directory + "/DATA/MISSIONS/pilots_population.ini"
        pilot_ini = self.parser.read(pilot_path)

        # check if there actually is a file there
        # (parser fails silently)
        if pilot_ini == []:
            messagebox.showerror("Error", "Failed to find pilots_populaiton.ini at specified location.")
            self.destroy()

        # return unique pilots
        pilots = [block['nickname'] for block in pilot_ini if 'nickname' in block]
        return list(set(list(itertools.chain.from_iterable(pilots))))
    

    def create_faction_list(self):

        faction_path = self.install_directory + "/DATA/MISSIONS/faction_prop.ini" # Here os.path.join does not work, idk why
        faction_ini = self.parser.read(faction_path)
        
        # check
        if faction_ini == []:
            messagebox.showerror("Error", "Failed to find faction_prop.ini at specified location.")
            self.destroy()

        # return unique factions
        affiliations = [block['affiliation'] for block in faction_ini if 'affiliation' in block]
        return list(set(list(itertools.chain.from_iterable(affiliations))))
    

    def create_shipclass_list(self):

        ship_path = self.install_directory + "/DATA/MISSIONS/shipclasses.ini" # same again
        ship_ini = self.parser.read(ship_path)

        # Check if file there
        if ship_ini == []:
            messagebox.showerror("Error", "Failed to find shipclasses.ini at specified location.")
            self.destroy()

        # return unique shipclasses
        shipclasses = [block['member'] for block in ship_ini if 'member' in block]
        return list(set(list(itertools.chain.from_iterable(shipclasses))))
    

    def create_npcclass_list(self):
        npc_path = self.install_directory + "/DATA/MISSIONS/npcships.ini"
        npc_ini = self.parser.read(npc_path)

        # Tooodle-oo-do-doo
        if npc_ini == []:
            messagebox.showerror("Error", "Failed to find npcships.ini at specified location.")
            self.destroy()

        # return unique npc ships
        npc_classes = [block['npc_class'] for block in npc_ini if 'npc_class' in block]
        return list(set(list(itertools.chain.from_iterable(npc_classes))))
