from utils.static import Static
from pygame import Vector2
import math
from utils.kinematic_steering_output import KinematicSteeringOutput

class KinematicArrive:
    def __init__(self, character: Static, target: Static, maxSpeed: float, radius: float):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius
        self.timeToTarget = 0.25
    
    def get_steering(self) -> KinematicSteeringOutput:
        
        result = KinematicSteeringOutput(Vector2(0, 0), 0)
        
        # Se obtiene la dirección al objetivo
        result.velocity = self.target.position - self.character.position
        
        # Se chequea si estamos dentro del radio
        if result.velocity.magnitude() < self.radius:
            return None
        
        # Debemos movernos al objetivo, y queremos alcanzarlo en el tiempo timeToTarget en segundos
        result.velocity = result.velocity * (1 / self.timeToTarget)
        
        # Si es muy rápido, llevarlo a la máxima velocidad
        if result.velocity.magnitude() > self.maxSpeed:
            result.velocity = result.velocity.normalize() * self.maxSpeed
        
        # Cara a la dirección que queremos movernos
        self.character.orientation = self.new_orientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result
    
    def new_orientation(self, current: float, velocity: Vector2) -> float:
        if velocity.magnitude() > 0:
            return math.atan2(velocity.y, velocity.x)
        else:
            return current