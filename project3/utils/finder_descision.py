from typing import Dict, Tuple
from utils.decision_tree import Action
from utils.static import Static
from utils.kinematic import Kinematic
from pygame import Vector2
from utils.face import Face

class FinderAction(Action):
    """
    ### Description
    An action that returns a Finder object.

    ### Attributes
    - `enemy`: dict
        The enemy's position and orientation.
    - `player`: tuple
        The player's position and orientation.
    ### Methods
    - `make_decision() -> str`
        Returns a "find" string.
    """
    def __init__(self, enemy: Dict[str, float|int], player: Tuple[int, int, float]):
        self.enemy: Dict[str, float|int] = enemy
        self.player: Tuple[int, int, float] = player
        
    def make_decision(self) -> str|None:
        return "find"

class FaceAction(Action):
    """
    ### Description
    An action that returns a Face object.

    ### Attributes
    - `enemy`: dict
        The enemy's position and orientation.
    - `player`: tuple
        The player's position and orientation.
    - `maxAngularAcceleration`: float
        The maximum angular acceleration of the enemy.
    - `maxRotation`: float
        The maximum rotation of the enemy.
    - `targetRadius`: float
        The radius to consider the target as reached.
    - `slowRadius`: float
        The radius to start slowing down.

    ### Methods
    - `make_decision() -> Face`
        Returns a Face object.
    """
    def __init__(self, enemy: Dict[str, float|int], player: Tuple[int, int, float], maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float):
        self.enemy: Dict[str, float|int] = enemy
        self.player: Tuple[int, int, float] = player
        self.max_angular_acceleration: float = maxAngularAcceleration
        self.max_rotation: float = maxRotation
        self.target_radius: float = targetRadius
        self.slowRadius: float = slowRadius
        
    def make_decision(self) -> Face:
        enemy_static: Static = Kinematic(Vector2(self.enemy["x"], self.enemy["y"]), self.enemy["orientation"])
        player_static: Static = Kinematic(Vector2(self.player[0], self.player[1]), self.player[2])
        
        return Face(
            enemy_static,
            player_static,
            self.max_angular_acceleration,
            self.max_rotation,
            self.target_radius,
            self.slowRadius
        )