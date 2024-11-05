from typing import Callable, List
from utils.decision_tree import Action, Decision
from utils.static import Static
from pygame import Vector2
from utils.kinematic_arrive import KinematicArrive
import math

class KinematicArriveAction(Action):
    """
    ### Description
    An action that returns a KinematicArrive object.

    ### Attributes
    - `enemy`: dict
        The enemy's position.
    - `player`: tuple
        The player's position.
    - `max_speed`: float
        The maximum speed of the enemy.
    - `arrival_radius`: float
        The radius at which the enemy will stop.

    ### Methods
    - `make_decision() -> KinematicArrive`
        Returns a KinematicArrive object
    """
    def __init__(self, enemy, player, max_speed, arrival_radius):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.arrival_radius = arrival_radius
        
    def make_decision(self):
        enemy_static = Static(Vector2(self.enemy["x"], self.enemy["y"]), 0)
        player_static = Static(Vector2(self.player[0], self.enemy["y"]), 0)
        return KinematicArrive(enemy_static, player_static, self.max_speed, self.arrival_radius)

class PatrolAction(Action):
    """
    ### Description
    An action that returns a string "patrol".

    ### Attributes
    - `enemy`: dict
        The enemy's position.
    - `direction`: str
        The direction the enemy is facing.

    ### Methods
    - `make_decision() -> str`
        Returns "patrol".
    """
    def __init__(self, enemy, direction):
        self.enemy = enemy
        self.direction = direction
        
    def make_decision(self):
        return "patrol"

class InRangeDecision(Decision):
    """
    ### Description
    A decision that returns the result of a test function.

    ### Attributes
    - `enemy_pos`: Vector2
        The enemy's position.
    - `player_pos`: Vector2
        The player's position.
    - `true_node`: Decision
        The decision to return if the test function returns True.
    - `false_node`: Decision
        The decision to return if the test function returns False.
    - `test_function`: function
    """
    def __init__(self, enemy_pos: Vector2, player_pos: Vector2, true_node: Decision, false_node: Decision, test_function: Callable):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.test_function = test_function
        
    def test_value(self):
        return self.test_function(self.enemy_pos, self.player_pos)

class AttackAction(Action):
    """
    ### Description
    An action that returns a string "attack".

    ### Attributes
    - `enemy`: dict
        The enemy's position.
    - `direction`: str
        The direction the enemy is facing.
    - `attack_sprites_right`: list
        A list of sprites for the enemy facing right.
    - `attack_sprites_left`: list
        A list of sprites for the enemy facing left.
    """
    def __init__(self, enemy, direction: str, attack_sprites_right: List[str], attack_sprites_left: List[str]):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        print("Attack action triggered!")
        return "attack"

class PlayerReachedDecision(Decision):
    """
    ### Description
    A decision that returns the result of a test function.

    ### Attributes
    - `enemy_pos`: Vector2
        The enemy's position.
    - `player_pos`: Vector2
        The player's position.
    - `true_node`: Decision
        The decision to return if the test function returns True.
    - `false_node`: Decision
        The decision to return if the test function returns False.
    - `arrival_radius`: float
        The radius at which the enemy will stop.

    ### Methods
    - `test_value() -> bool`
        Returns the result of the test function.
    """

    def __init__(self, enemy_pos: Vector2, player_pos: Vector2, true_node: Decision, false_node: Decision, arrival_radius: float):
        super().__init__(true_node, false_node)
        self.enemy_pos = enemy_pos
        self.player_pos = player_pos
        self.arrival_radius = arrival_radius
        
    def test_value(self):
        dx: int = self.player_pos[0] - self.enemy_pos[0]
        dy: int = self.player_pos[1] - self.enemy_pos[1]
        distance: float = math.sqrt(dx*dx + dy*dy)
        return isinstance(self.false_node.make_decision(), KinematicArrive) and distance <= self.arrival_radius

class AttackAction(Action):
    """
    ### Description
    An action that returns a string "attack".

    ### Attributes
    - `enemy`: dict
        The enemy's position.
    - `direction`: str
        The direction the enemy is facing.
    - `attack_sprites_right`: list
        A list of sprites for the enemy facing right.
    - `attack_sprites_left`: list
        A list of sprites for the enemy facing left.
    """
    def __init__(self, enemy, direction: str, attack_sprites_right: List, attack_sprites_left: List):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        return "attack"
