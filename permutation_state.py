
from dataclasses import dataclass
from typing import Union, List


class Permutation_State:
    """
        For Saving and Loading Permutations a user has created.
    """
    def __init__(self, name = "Default"):
        self.name = name
        self.ship_by_class = "Ship by class"
        self.min_max = ["INT","INT"]
        self.job_override = "Job Override"
        self.class_override = "Class Override"
        self.formation = "Formation"
        self.simultaneous_creation = "Simultaneous Creation"
        self.behaviour = "Behaviour"
        self.creation_distance = "INT"
        self.permutation_weight = "INT"
        self.arrival_types = [0, 0, 0, 0, 0, 0, 0, 0]
        self.faction = ["Faction", "%", "INT"]
        self.density_restriction = ["Density Restriction", "INT"]
        self.relief = "INT"
        self.repop = "INT"
        self.density = "INT"
        #self.spawn_chance = "%"