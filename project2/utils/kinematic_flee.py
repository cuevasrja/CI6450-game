from utils.static import Static
from pygame import Vector2
from utils.kinematic_steering_output import KinematicSteeringOutput
import math

class KinematicFlee:
    """
    ### Description
    A class that implements the Kinematic Flee behavior.

    ### Attributes
    - `character`: Static
        The character that is fleeing.
    - `target`: Static
        The target to flee from.
    - `maxSpeed`: float
        The maximum speed of the character.
    - `maxDistance`: float
        The distance at which the character will flee.
    - `screen_width`: int
        The width of the screen.

    ### Methods
    - `get_steering() -> KinematicSteeringOutput`
        Returns the steering output for the character.
    - `get_edge_force() -> Vector2`
        Returns the force to avoid the edges of the screen.
    - `new_orientation(current: float, velocity: Vector2) -> float`
        Returns the new orientation of the character.
    """
    def __init__(self, character: Static, target: Static, maxSpeed: float, maxDistance: float, screen_width: int, screen_height: int):
        self.character: Static = character
        self.target: Static = target
        self.maxSpeed: float = maxSpeed
        self.maxDistance: float = maxDistance
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
    
    def get_steering(self) -> KinematicSteeringOutput:
        result = KinematicSteeringOutput(Vector2(0, 0), 0)
        
        direction: Vector2 = self.character.position - self.target.position
        distance: float = direction.magnitude()
        
        if distance > 0:
            result.velocity = direction.normalize() * self.maxSpeed
        
        # Add edge force
        edge_force: Vector2 = self.get_edge_force()
        result.velocity += edge_force
        
        # Update orientation
        self.character.orientation = self.new_orientation(self.character.orientation, result.velocity)
        result.rotation = 0
        
        return result
    
    def get_edge_force(self) -> Vector2:
        force: Vector2 = Vector2(0, 0)
        edge_distance: int = 50  # Distance from the edge at which to start avoiding it

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