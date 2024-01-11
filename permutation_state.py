
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Permutation_State:
    """
        For Saving and Loading Permutations a user has created.
    """
    ship_by_class : str
    min_max : Tuple[int, int]
    job_override : str
    class_override : str
    formation : str
    simultanious_creation : str
    behaviour : str
    creation_distance : int
    permutation_weight : int
    arrival_types : Tuple[bool]
    faction : Tuple[str, float, int]
    density_restriction : Tuple[str, int]
    relief : int
    repop : int
    density : int
    spawn_chance : float
