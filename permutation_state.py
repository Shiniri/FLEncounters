
from dataclasses import dataclass
from typing import Union, List


class Permutation_State:
    """
        For Saving and Loading Permutations a user has created.
    """
    def __init__(self):
        self.name : str = "Default"
        self.ship_by_class : str = "Ship by class"
        self.min_max : List[int] = [1,2]
        self.job_override : str = "Job Override"
        self.class_override : str = "Class Override"
        self.formation : str = "Formation"
        self.simultanious_creation : str = "Simultanious Creation"
        self.behaviour : str = "Behaviour"
        self.creation_distance : int = 1
        self.permutation_weight : int = 1
        self.arrival_types : List[bool] = (False, False, False, False, False, False, False, False)
        self.faction : List[Union[str, float, int]] = ["Faction", 0.5, 1]
        self.density_restriction : List[Union[str, int]] = ["Density Restriction", 1]
        self.relief : int = 1
        self.repop : int = 1
        self.density : int = 1
        self.spawn_chance : float = 0.0

    # Dropdowns
    def on_ship_select(self, event):
        self.ship_by_class = event.widget.get()
    def on_job_override_select(self, event):
        self.job_override = event.widget.get()
    def on_class_override_select(self, event):
        self.class_override = event.widget.get()
    def on_formation_select(self, event):
        self.formation = event.widget.get()
    def on_simultanious_creation_select(self, event):
        self.simultanious_creation = event.widget.get()
    def on_behaviour_select(self, event):
        self.behaviour = event.widget.get()
    def on_faction_select(self, event):
        self.faction[0] = event.widget.get()
    def on_density_restriction_select(self, event):
        self.density_restriction[0] = event.widget.get()