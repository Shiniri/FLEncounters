
# GUI
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Button, Listbox

from custom_widgets import (
    FactionSelector, 
    DensityRestrictionSelector, 
    VariableFrame,
    Core_Encounter_Specs,
    Rename_Popup,
    Spawnable_Ships_List
)
from permutation_state import Permutation_State

# Parsing
from ini_parser import Ini_Parser

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
        self.geometry("620x490")
        # Handles saving data the user has entered
        self.permutation_states = []
        default_permutation_state = Permutation_State()
        self.current_permutation_state = default_permutation_state

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
        self.available_pilots = self.create_list_from_ini_field("pilots_population.ini", "nickname")
        self.available_factions = self.create_list_from_ini_field("faction_prop.ini", "affiliation")
        self.available_shipclasses = self.create_list_from_ini_field("shipclasses.ini", "member")
        self.available_npcclasses = self.create_list_from_ini_field("npcships.ini", "npc_class")
        self.available_formations = self.create_list_from_ini_field("formations.ini","nickname")


        #   RIGHT / PERMUTATIONS COLUMN     #
        
        self.permutation_listbox = Listbox(self.right_frame, selectmode="SINGLE", exportselection=False)
        self.permutation_listbox.pack(pady=10)

        def _on_new_permutation():
            self.permutation_states.append(Permutation_State(f"Default {len(self.permutation_states)+1}"))
            self.permutation_listbox.insert(0, f"Default {len(self.permutation_states)}")
            self.permutation_listbox.selection_clear(0, "end")
            self.permutation_listbox.selection_set(0)
            self.permutation_listbox.event_generate("<<ListboxSelect>>")
            

        self.add_permutation_button = Button(self.right_frame, text="New Permutation", command=_on_new_permutation)
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

        # Spawnable Ships list
        self.spawnable_ships = Spawnable_Ships_List(parent=self.centre_frame)
        self.spawnable_ships.pack(pady=10)


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

        # Create Encounter
        def _create_encounter_ini():
            for permutation in self.permutation_states:
                base_encounter_formation_str = (
                    "[EncounterFormation]"
                    f"ship_by_class = {permutation.min_max[0]}, {permutation.min_max[1]}, {permutation.ship_by_class}"
                )
        self.create_encounter_button.configure(command=_create_encounter_ini)

        # Permutation Selector
        # Permutation in the next function refers to the global var /
        # class, not the listbox entry!!
        def _get_and_set_permutation_index(permutation_name):
            for permutation in self.permutation_states:
                if permutation.name == permutation_name:
                    self.current_permutation_state = permutation
                    return permutation

        def _get_permutation_index(permutation_name):
            for permutation_index in range(len(self.permutation_states)):
                if self.permutation_states[permutation_index].name == permutation_name:
                    return permutation_index
                
        def _update_window_by_permutation(permutation):
            # Name
            selected_index = self.permutation_listbox.curselection()[0]
            self.permutation_listbox.delete(selected_index)
            self.permutation_listbox.insert(selected_index, self.current_permutation_state.name)
            self.permutation_listbox.select_set(selected_index)

            # Dropdowns 
            self.core_encounter_settings.ship_by_class_dropdown.set(permutation.ship_by_class)
            self.core_encounter_settings.job_override_dropdown.set(permutation.job_override)
            self.core_encounter_settings.class_override_dropdown.set(permutation.class_override)
            self.core_encounter_settings.formation_dropdown.set(permutation.formation)
            self.core_encounter_settings.simultaneous_creation_dropdown.set(permutation.simultaneous_creation)
            self.core_encounter_settings.behaviour_combobox.set(permutation.behaviour)
            
            self.faction_selector.dropdown.set(permutation.faction[0])
            self.density_restriction_selector.dropdown.set(permutation.density_restriction[0])

            # INT fields
            self.core_encounter_settings.min_max_setter.entry_max_var.set(self.current_permutation_state.min_max[1])
            self.core_encounter_settings.min_max_setter.entry_min_var.set(self.current_permutation_state.min_max[0])
            self.core_encounter_settings.creation_distance_setter.entry_var.set(self.current_permutation_state.creation_distance)
            self.core_encounter_settings.permutation_weight_setter.entry_var.set(self.current_permutation_state.permutation_weight)
            
            self.faction_selector.entry1_var.set(self.current_permutation_state.faction[1])
            self.faction_selector.entry2_var.set(self.current_permutation_state.faction[2])
            self.density_restriction_selector.entry1_var.set(self.current_permutation_state.density_restriction[1])
            self.variable_frame.relief_time_setter.entry_var.set(self.current_permutation_state.relief)
            self.variable_frame.repop_time_setter.entry_var.set(self.current_permutation_state.repop)
            self.variable_frame.density_setter.entry_var.set(self.current_permutation_state.density)

            # Checkboxes
            for i, arrival_type_var in enumerate(self.core_encounter_settings.button_vars):
                arrival_type_var.set(self.current_permutation_state.arrival_types[i])

        def _listbox_callback(event):
            permutation_name = event.widget.get(event.widget.curselection()[0])
            _update_window_by_permutation(_get_and_set_permutation_index(permutation_name))
                
        self.permutation_listbox.bind(
            "<<ListboxSelect>>",
            _listbox_callback
        )

        # Rename Permutation
        # This is so fucking disgusting
        def _on_rename_permutation():
            top = Rename_Popup(self)
            top.geometry("250x100")
            top.title("Rename Permutation")
            def _rename():
                existing_names = [permutation_state.name for permutation_state in self.permutation_states]
                entered_name = top.rename_entry_var.get()
                if entered_name in existing_names:
                    messagebox.showerror("Error", "This permutation name already exists.")
                else:
                    self.current_permutation_state.name = entered_name
                    _update_window_by_permutation(self.current_permutation_state)
                top.destroy()
            top.save_button.configure(command=_rename)
            top.mainloop()
        self.rename_permutation_button.configure(text="Rename Permutation", command=_on_rename_permutation)

        # Delete Permutation
        def _on_delete_permutation():
            corresponding_permutation_index = _get_permutation_index(self.permutation_listbox.get(self.permutation_listbox.curselection()[0]))
            self.permutation_states.pop(corresponding_permutation_index)
            self.permutation_listbox.delete(self.permutation_listbox.curselection()[0])
        self.delete_permutation_button.configure(command=_on_delete_permutation)

        # Dropdowns
        def _on_ship_select(event):
            self.current_permutation_state.ship_by_class = event.widget.get()
        def _on_job_select(event):
            self.current_permutation_state.job_override = event.widget.get()
        def _on_class_select(event):
            self.current_permutation_state.class_override = event.widget.get()
        def _on_formation_select(event):
            self.current_permutation_state.formation = event.widget.get()
        def _on_simultaneous_creation_select(event):
            self.current_permutation_state.simultaneous_creation = event.widget.get()
        def _on_behaviour_select(event):
            self.current_permutation_state.behaviour = event.widget.get()
        def _on_faction_select(event):
            self.current_permutation_state.faction[0] = event.widget.get()
        def _on_density_restriction_select(event):
            self.current_permutation_state.density_restriction[0] = event.widget.get()

        self.core_encounter_settings.ship_by_class_dropdown.bind("<<ComboboxSelected>>", _on_ship_select)
        self.core_encounter_settings.job_override_dropdown.bind("<<ComboboxSelected>>", _on_job_select)
        self.core_encounter_settings.class_override_dropdown.bind("<<ComboboxSelected>>", _on_class_select)
        self.core_encounter_settings.formation_dropdown.bind("<<ComboboxSelected>>", _on_formation_select)
        self.core_encounter_settings.simultaneous_creation_dropdown.bind("<<ComboboxSelected>>", _on_simultaneous_creation_select)
        self.core_encounter_settings.behaviour_combobox.bind("<<ComboboxSelected>>", _on_behaviour_select)
        self.faction_selector.dropdown.bind("<<ComboboxSelected>>", _on_faction_select)
        self.density_restriction_selector.dropdown.bind("<<ComboboxSelected>>", _on_density_restriction_select)

        # Entry fields
        def _on_min_select(event):
            self.current_permutation_state.min_max[0] = event.widget.get()
        def _on_max_select(event):
            self.current_permutation_state.min_max[1] = event.widget.get()
        def _on_creation_distance_select(event):
            self.current_permutation_state.creation_distance = event.widget.get()
        def _on_permutation_weight_select(event):
            self.current_permutation_state.permutation_weight = event.widget.get()
        def _on_faction_percentage_select(event):
            self.current_permutation_state.faction[1] = event.widget.get()
        def _on_faction_int_select(event):
            self.current_permutation_state.faction[2] = event.widget.get()
        def _on_density_restriction_int_select(event):
            self.current_permutation_state.density_restriction[1] = event.widget.get()
        def _on_relief_time_select(event):
            self.current_permutation_state.relief = event.widget.get()
        def _on_repop_time_select(event):
            self.current_permutation_state.repop = event.widget.get()
        def _on_density_select(event):
            self.current_permutation_state.density = event.widget.get()

        self.core_encounter_settings.min_max_setter.entry_min.bind("<FocusOut>", _on_min_select)
        self.core_encounter_settings.min_max_setter.entry_max.bind("<FocusOut>", _on_max_select)
        self.core_encounter_settings.creation_distance_setter.entry.bind("<FocusOut>", _on_creation_distance_select)
        self.core_encounter_settings.permutation_weight_setter.entry.bind("<FocusOut>", _on_permutation_weight_select)
        self.faction_selector.entry1.bind("<FocusOut>", _on_faction_percentage_select)
        self.faction_selector.entry2.bind("<FocusOut>", _on_faction_int_select)
        self.density_restriction_selector.entry1.bind("<FocusOut>", _on_density_restriction_int_select)
        self.variable_frame.relief_time_setter.entry.bind("<FocusOut>", _on_relief_time_select)
        self.variable_frame.repop_time_setter.entry.bind("<FocusOut>", _on_repop_time_select)
        self.variable_frame.density_setter.entry.bind("<FocusOut>", _on_density_select)

        # Arrival Type
        def _on_arrival_type_select(event):
            # No permutation state selected
            if self.current_permutation_state == None:
                return
            for i, variable in enumerate(self.core_encounter_settings.button_vars):
                self.current_permutation_state.arrival_types[i] = variable.get()
        for arrival_type_button in self.core_encounter_settings.buttons:
            arrival_type_button.bind(
                "<Leave>",
                _on_arrival_type_select
            )

        # Create encounter button
            
        # Apparently this is the python way to do this
        def _is_int(num):
            try:
                int(num)
                return True
            except:
                return False
            
        def _is_float(num):
            try:
                float(num)
                return True
            except:
                return False
            

        def _validate(permutation):
            # Has user set a ship class? / Is it still the default values?
            # 1. Grab all default values from the permutation state class
            default_permutation = Permutation_State()
            default_permutation_vars = {key:value for key, value in default_permutation.__dict__.items() if not key.startswith('__') and not callable(key)}
            current_permutation_vars = {key:value for key, value in permutation.__dict__.items() if not key.startswith('__') and not callable(key)}

            for default_key in default_permutation_vars.keys():
                # These settings do not have to be specified / are valid defaults
                if default_key == "name" or default_key == "arrival_types":
                    continue
                # This means it's still the default setting
                if default_permutation_vars[default_key] == current_permutation_vars[default_key]:
                    messagebox.showerror("Error", f"You haven't provided a valid value for the setting {default_key} in permutation '{permutation.name}'.")
                    return False
                
            # Are all entry fields convertible to the types needed in the permutation state?
            if not _is_int(permutation.min_max[0]) or not _is_int(permutation.min_max[1]):
                messagebox.showerror("Error", f"Please provide an Integer value in the min max field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.creation_distance):
                messagebox.showerror("Error", f"Please provide an Integer value in the creation distance field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.permutation_weight):
                messagebox.showerror("Error", f"Please provide an Integer value in the permutation weight field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.faction[2]):
                messagebox.showerror("Error", f"Please provide an Integer value in the faction field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.density_restriction[1]):
                messagebox.showerror("Error", f"Please provide an Integer value in the density restriction field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.relief):
                messagebox.showerror("Error", f"Please provide an Integer value in the relief field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.repop):
                messagebox.showerror("Error", f"Please provide an Integer value in the repop field of permutation '{permutation.name}'.")
                return False
            if not _is_int(permutation.density):
                messagebox.showerror("Error", f"Please provide an Integer value in the density field of permutation '{permutation.name}'.")
                return False
            if not _is_float(permutation.faction[1]):
                messagebox.showerror("Error", f"Please provide a Float(-convertible) value in the faction field of permutation '{permutation.name}'.")
                return False
            
            return True

        def _on_encounter_create():

            # Construct the encounter string from all existing permutations
            full_encounter = ""
            # I know this button thing is dumb, but there is a reason for it:
            # tkinter checkbuttons apparently have no 'text' attribute, even
            # though you set it upon creation, but whatever...
            button_texts = [
                "buzz", "cruise", "object_all", "tradelane",
                "object_capital", "object_station", "object_jump_gate",
                "object_docking_ring"
            ]   

            for permutation_state in self.permutation_states:
                if not _validate(permutation_state):
                    return
                base_str = (
                    f"[{permutation_state.name}]\n"
                    f"ship_by_class = {permutation_state.min_max[0]}, {permutation_state.min_max[1]}, {permutation_state.ship_by_class}\n"
                    f"pilot_job = {permutation_state.job_override}\n"
                    f"formation_by_class = {permutation_state.formation}\n"
                    f"behaviour = {permutation_state.behaviour}\n"
                    f"allow_simultaneous_creation = {permutation_state.simultaneous_creation}\n"
                )
                arrival_type_str = "arrival = " + ", ".join([button_text for i, button_text in enumerate(button_texts) if permutation_state.arrival_types[i] == 1])
                solar_str = (
                    "; UNCOMMENT AND ADD IN APPROPRIATE SOLAR. THIS WILL BE IMPROVED IN A LATER VERSION :)\n"
                    f";density = {permutation_state.density}\n"
                    f";repop_time = {permutation_state.repop}\n"
                    f";relief_time = {permutation_state.relief}\n"
                    f";faction = {permutation_state.faction[0]}\n"
                    f";density_restriction = {permutation_state.density_restriction}\n"
                    ";max_battle_size = 8\n"
                    ";encounter_name = some_nick"
                )   #TODO max_battle_size as setable parameter in the GUI
                    #TODO encounter name
                full_encounter += (base_str+arrival_type_str+"\n\n"+solar_str+"\n\n")
            with filedialog.asksaveasfile(title="Please select an encounter file to save in.") as encounter_file:
                encounter_file.write(full_encounter)
        self.create_encounter_button.configure(command=_on_encounter_create)
                

    def create_list_from_ini_field(self, filename, field_name):

        target_path = self.install_directory + "/DATA/MISSIONS/" + filename
        ini_file = self.parser.read(target_path)

        # Check if file is actually there
        # (parser fails silently / outputs [])
        if ini_file == []:
            messagebox.showerror("Error", f"Failed to find {filename} at specified location.")
            self.destroy()

        # Return unique values for field
        values = [block[field_name] for block in ini_file if field_name in block]
        return list(set(list(itertools.chain.from_iterable(values))))