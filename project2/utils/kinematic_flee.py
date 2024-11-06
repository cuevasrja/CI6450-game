from utils.static import Static
from pygame import Vector2
from utils.kinematic_steering_output import KinematicSteeringOutput
import math

class KinematicFlee:
    def __init__(self, character: Static, target: Static, maxSpeed: float, maxDistance: float, screen_width: int, screen_height: int):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.maxDistance = maxDistance
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def get_steering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector2(0, 0), 0)
        
        direction = self.character.position - self.target.position
        distance = direction.magnitude()
        
        if distance > 0:
            result.velocity = direction.normalize() * self.maxSpeed
        
        # Añadir una fuerza para alejarse de los bordes
        edge_force = self.get_edge_force()
        result.velocity += edge_force
        
        self.character.orientation = self.new_orientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result
    
    def get_edge_force(self) -> Vector2:
        force = Vector2(0, 0)
        edge_distance = 50  # Distancia desde el borde para empezar a aplicar la fuerza

        if self.character.position.x < edge_distance:
            force.x += self.maxSpeed * (1 - self.character.position.x / edge_distance)
        elif self.character.position.x > self.screen_width - edge_distance:
            force.x -= self.maxSpeed * (1 - (self.screen_width - self.character.position.x) / edge_distance)

        if self.character.position.y < edge_distance:
            force.y += self.maxSpeed * (1 - self.character.position.y / edge_distance)
        elif self.character.position.y > self.screen_height - edge_distance:
            force.y -= self.maxSpeed * (1 - (self.screen_height - self.character.position.y) / edge_distance)

        return force
        
    def new_orientation(self, current: float, velocity: Vector2) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.y, velocity.x)
        else:
            return current