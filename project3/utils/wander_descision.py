from typing import Dict, Tuple
from utils.decision_tree import Action
from utils.steering_output import SteeringOutput
from utils.static import Static
from utils.kinematic import Kinematic
from pygame import Vector2
from utils.wander import Wander
from utils.face import Face

class WanderAction(Action):
    """
    ### Description
    An action that returns a Wander object.

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
    - `wanderOffset`: float
        The offset to wander.
    - `wanderRadius`: float
        The radius to wander.
    - `wanderRate`: float
        The rate to wander.
    - `wanderOrientation`: float
        The orientation to wander.
    - `maxAcceleration`: float
        The maximum acceleration of the enemy.
    ### Methods
    - `make_decision() -> Wander|None`
        Returns a Wander object if the player is within the max distance.
    """
    def __init__(self, enemy: Dict[str, float|int], player: Tuple[int, int, float], maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, wanderOffset: float, wanderRadius: float, wanderRate: float, wanderOrientation: float, maxAcceleration: float):
        self.enemy: Dict[str, float|int] = enemy
        self.player: Tuple[int, int, float] = player
        self.max_angular_acceleration: float = maxAngularAcceleration
        self.max_rotation: float = maxRotation
        self.target_radius: float = targetRadius
        self.slowRadius: float = slowRadius
        self.wanderOffset: float = wanderOffset
        self.wanderRadius: float = wanderRadius
        self.wanderRate: float = wanderRate
        self.wanderOrientation: float = wanderOrientation
        self.maxAcceleration: float = maxAcceleration
        
    def make_decision(self) -> Wander|None:
        # enemy_static: Static = Kinematic(Vector2(self.enemy["x"], self.enemy["y"]), self.enemy["orientation"])
        # player_static: Static = Kinematic(Vector2(self.player[0], self.player[1]), self.player[2])
        
        # wander: Wander = Wander(
        #     enemy_static,
        #     player_static,
        #     self.max_angular_acceleration,
        #     self.max_rotation,
        #     self.target_radius,
        #     self.slowRadius,
        #     self.wanderOffset,
        #     self.wanderRadius,
        #     self.wanderRate,
        #     self.wanderOrientation,
        #     self.maxAcceleration
        # )

        # return wander
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
        
class EnemyAttackAction(Action):
    """
    ### Description
    An action that returns an EnemyAttackAction object.

    ### Attributes
    - `enemy`: dict
        The enemy's position.
    - `direction`: str
        The direction the enemy is facing.
    - `attack_sprites_right`: str
        The sprites for the enemy attacking to the right.
    - `attack_sprites_left`: str
        The sprites for the enemy attacking to the left.

    ### Methods
    - `make_decision() -> str`
        Returns "attack" to indicate that the enemy is attacking.
    """
    def __init__(self, enemy: Vector2, direction: str, attack_sprites_right: str, attack_sprites_left: str):
        self.enemy: Vector2 = enemy
        self.direction: str = direction
        self.attack_sprites_right: str = attack_sprites_right
        self.attack_sprites_left: str = attack_sprites_left
        
    def make_decision(self) -> str:
        self.enemy["is_attacking"] = True
        return "attack"

class PlayerAttackingDecision:
    """
    ### Description
    A decision that returns a WanderAction or an EnemyAttackAction.

    ### Attributes
    - `wander_action`: WanderAction
        The action to take when the player is attacking.
    - `attack_action`: EnemyAttackAction
        The action to take when the player is not attacking.

    ### Methods
    - `make_decision(is_player_attacking: bool) -> WanderAction|EnemyAttackAction`
        Returns the appropriate action based on whether the player is attacking.
    """
    def __init__(self, wander_action: WanderAction, attack_action: EnemyAttackAction):
        self.wander_action: WanderAction = wander_action
        self.attack_action: EnemyAttackAction = attack_action
        
    def make_decision(self, is_player_attacking) -> WanderAction|EnemyAttackAction:
        if is_player_attacking:
            return self.wander_action
        return self.attack_action