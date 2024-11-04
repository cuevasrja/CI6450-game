import random
from pygame import Vector2
from utils.trigonometry import new_orientation, in_radius, magnitude, normalize, rotate_vector
from utils.physics import KinematicSteeringOutput, Static

class KinematicSeek:
    """
    ### Description
    A class to represent a seek behavior.

    ### Attributes
    - `character` : Static : The character to move.
    - `target` : Static : The target to seek.
    - `max_speed` : float : The maximum speed of the character.

    ### Methods
    - `get_steering() -> KinematicSteeringOutput` : Returns the steering to seek the target.
    """
    def __init__(self, character: Static, target: Static, max_speed: float):
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        # The direction is set to the target position minus the character position.
        steering.velocity = self.target.position - self.character.position
        # The direction is normalized and multiplied by the maximum speed.
        steering.velocity = normalize(steering.velocity) * self.max_speed

        # The orientation is set to the angle of the linear direction.
        self.character.orientation = new_orientation(self.character.orientation, steering.velocity)

        # The angular is set to 0.
        steering.rotation = 0
        return steering
    
class KinematicFlee: # This is the same as KinematicSeek, but with the direction reversed.
    """
    ### Description
    A class to represent a flee behavior.

    ### Attributes
    - `character` : Static : The character to move.
    - `target` : Static : The target to flee.
    - `max_speed` : float : The maximum speed of the character.

    ### Methods
    - `get_steering() -> KinematicSteeringOutput` : Returns the steering to flee the target.
    """
    def __init__(self, character: Static, target: Static, max_speed: float):
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        # The direction is reversed.
        steering.velocity = self.character.position - self.target.position
        # The direction is normalized and multiplied by the maximum speed.
        steering.velocity = normalize(steering.velocity) * self.max_speed

        # The orientation is set to the angle of the linear direction.
        self.character.orientation = new_orientation(self.character.orientation, steering.velocity)

        # The angular is set to 0.
        steering.rotation = 0
        return steering

class KinematicArrive:
    """
    ### Description
    A class to represent an arrive behavior.

    ### Attributes
    - `character` : Static : The character to move.
    - `target` : Static : The target to arrive.
    - `max_speed` : float : The maximum speed of the character.
    - `radius` : float : The satisfaction radius.
    - `timeToTarget` : float : The time to target. (default 0.25)

    ### Methods
    - `get_steering() -> KinematicSteeringOutput` : Returns the steering to arrive at the target.
    """
    def __init__(self, character: Static, target: Static, max_speed: float, radius: float) -> None:
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed
        self.satisfaction_radius = radius

    # The time to target constant.
    timeToTarget: float = 0.25

    def get_steering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Get the direction to the target.
        result.velocity = self.target.position - self.character.position

        # Check if we are within the satisfaction radius.
        if in_radius(result.velocity, self.satisfaction_radius):
            result.velocity = Vector2(0, 0)
            return result

        # If we are outside the satisfaction radius, calculate the target speed.
        result.velocity /= self.timeToTarget

        # If the target speed is greater than the max speed, then clip it.
        if magnitude(result.velocity) > self.max_speed:
            result.velocity = normalize(result.velocity) * self.max_speed

        # Set the orientation to the direction.
        self.character.orientation = new_orientation(self.character.orientation, result.velocity)

        # Set the rotation to 0.
        result.rotation = 0
        return result
    
class KinematicWander:
    """
    ### Description
    A class to represent a wander behavior.

    ### Attributes
    - `character` : Static : The character to move.
    - `max_speed` : float : The maximum speed of the character.
    - `max_rotation` : float : The maximum rotation of the character.

    ### Methods
    - `get_steering() -> KinematicSteeringOutput` : Returns the steering to wander around.
    """
    def __init__(self, character: Static, max_speed: float, max_rotation: float = 0):
        self.character: Static = character
        self.max_speed: float = max_speed
        self.max_rotation: float = max_rotation

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        # Set the velocity to the character's orientation.
        steering.velocity = Vector2(1, 0)
        # Rotate the velocity by a random angle.
        steering.velocity = rotate_vector(steering.velocity, self.character.orientation)
        # Multiply the velocity by the maximum speed.
        steering.velocity *= self.max_speed

        # Set the orientation to the velocity.
        steering.rotation = (random.random() * 2 - 1) * self.max_rotation

        return steering

