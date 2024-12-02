from typing import Dict, Tuple
from utils.decision_tree import Action
from utils.steering_output import SteeringOutput
from utils.static import Static
from utils.kinematic import Kinematic
from pygame import Vector2
from utils.flee import Flee

class FleeAction(Action):
    """
    ### Description
    An action that returns a KinematicFlee object.

    ### Attributes
    - `enemy`: dict
        The enemy's position and orientation.
    - `player`: tuple
        The player's position and orientation.
    - `max_speed`: float
        The maximum speed of the enemy.
    - `max_distance`: float
        The distance at which the enemy will flee.
    - `screen_width`: int
        The width of the screen.
    - `screen_height`: int
        The height of the screen.
    - `min_x`: int
        The minimum x value the enemy can move to.
    - `max_x`: int
        The maximum x value the enemy can move to.

    ### Methods
    - `make_decision() -> KinematicFlee|None`
        Returns a KinematicFlee object if the player is within the max distance.
    """
    def __init__(self, enemy: Dict[str, float|int], player: Tuple[int, int, float], max_speed: float, max_distance: float, screen_width: int, screen_height: int, min_x: int, max_x: int):
        self.enemy: Vector2 = enemy
        self.player: Vector2 = player
        self.max_speed: float = max_speed
        self.max_distance: float = max_distance
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.min_x: int = min_x
        self.max_x: int = max_x
        
    def make_decision(self) -> Flee|None:
        enemy_static: Static = Kinematic(Vector2(self.enemy["x"], self.enemy["y"]), self.enemy["orientation"])
        
        player_static: Static = Static(Vector2(self.player[0], self.player[1]), 0)
        
        dx: int = self.enemy["x"] - self.player[0]
        dy: int = self.enemy["y"] - self.player[1]
        distance: float = (dx*dx + dy*dy)**0.5

        # If the player is within the max distance, flee 
        if distance <= self.max_distance:
            flee_behavior = Flee(
                enemy_static,
                player_static,
                self.max_speed
            )
        
            # Update the enemy's position
            steering: SteeringOutput = flee_behavior.get_steering()
            if steering:
                new_x: int = self.enemy["x"] + steering.linear.x
                new_y: int = self.enemy["y"] + steering.linear.y
                # Limitate the enemy's movement to the screen width
                if self.min_x <= new_x <= self.max_x:
                    self.enemy["x"] = new_x
                    self.enemy["y"] = new_y
                    
            return flee_behavior
        return None
        
        
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
    A decision that returns a KinematicFleeAction or an EnemyAttackAction.

    ### Attributes
    - `flee_action`: KinematicFleeAction
        The action to take when the player is attacking.
    - `attack_action`: EnemyAttackAction
        The action to take when the player is not attacking.

    ### Methods
    - `make_decision(is_player_attacking: bool) -> KinematicFleeAction|EnemyAttackAction`
        Returns the appropriate action based on whether the player is attacking.
    """
    def __init__(self, flee_action: FleeAction, attack_action: EnemyAttackAction):
        self.flee_action: FleeAction = flee_action
        self.attack_action: EnemyAttackAction = attack_action
        
    def make_decision(self, is_player_attacking) -> FleeAction|EnemyAttackAction:
        if is_player_attacking:
            return self.flee_action
        return self.attack_action