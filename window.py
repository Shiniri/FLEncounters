# GUI
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Typing
from typing import List, Dict

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
        available_factions : List[str] = self.create_faction_list()


    def create_faction_list(self) -> list(Dict[str, list]):

        faction_path : str = self.install_directory + "/DATA/MISSIONS/faction_prop.ini" # Here os.path.join does not work, idk why
        faction_ini = self.parser.read(faction_path)
        
        # check if there actually is a file there
        # (parser fails silently)
        if faction_ini == []:
            messagebox.showerror("Error", "Failed to find faction_prop.ini at specified location.")
            self.destroy()

        # return unique factions
        affiliations = [block['affiliation'] for block in faction_ini if 'affiliation' in block]
        return list(set(list(itertools.chain.from_iterable(affiliations))))

    
