from utils.decision_tree import Action
from utils.static import Static
from pygame import Vector2
from utils.kinematic_flee import KinematicFlee

class KinematicFleeAction(Action):
    def __init__(self, enemy, player, max_speed, max_distance, screen_width, screen_height, min_x, max_x):
        self.enemy = enemy
        self.player = player
        self.max_speed = max_speed
        self.max_distance = max_distance
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.min_x = min_x
        self.max_x = max_x
        
    def make_decision(self):
        enemy_static = Static(Vector2(self.enemy["x"], self.enemy["y"]), 0)
        
        player_static = Static(Vector2(self.player[0], self.player[1]), 0)
        
        dx = self.enemy["x"] - self.player[0]
        dy = self.enemy["y"] - self.player[1]
        distance = (dx*dx + dy*dy)**0.5
        
        if distance <= self.max_distance:
            flee_behavior = KinematicFlee(
                enemy_static,
                player_static,
                self.max_speed,
                self.max_distance,
                self.screen_width,
                self.screen_height
            )
        
            steering = flee_behavior.get_steering()
            if steering:
                new_x = self.enemy["x"] + steering.velocity.x
                # Limitamos el movimiento horizontal
                if self.min_x <= new_x <= self.max_x:
                    self.enemy["x"] = new_x
                    self.enemy["y"] = enemy_static.position.y
                    
            return flee_behavior
        return None
        
        
class EnemyAttackAction(Action):
    def __init__(self, enemy, direction, attack_sprites_right, attack_sprites_left):
        self.enemy = enemy
        self.direction = direction
        self.attack_sprites_right = attack_sprites_right
        self.attack_sprites_left = attack_sprites_left
        
    def make_decision(self):
        self.enemy["is_attacking"] = True
        return "attack"

class PlayerAttackingDecision:
    def __init__(self, flee_action, attack_action):
        self.flee_action = flee_action
        self.attack_action = attack_action
        
    def make_decision(self, is_player_attacking):
        if is_player_attacking:
            return self.flee_action
        return self.attack_action