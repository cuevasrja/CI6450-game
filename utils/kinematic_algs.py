import random
from pygame import Vector2
from utils.trigonometry import new_orientation, in_radius, magnitude, normalize, rotate_vector
from utils.physics import KinematicSteeringOutput, Static

class KinematicSeek:
    def __init__(self, character: Static, target: Static, max_speed: float):
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        steering.velocity = self.target.position - self.character.position
        steering.velocity = steering.velocity.normalize() * self.max_speed

        self.character.orientation = new_orientation(self.character.orientation, steering.velocity)

        steering.rotation = 0
        return steering
    
class KinematicFlee: # This is the same as KinematicSeek, but with the direction reversed.
    def __init__(self, character: Static, target: Static, max_speed: float):
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        steering.velocity = self.character.position - self.target.position
        steering.velocity = steering.velocity.normalize() * self.max_speed

        self.character.orientation = new_orientation(self.character.orientation, steering.velocity)

        steering.rotation = 0
        return steering

class KinematicArrive:
    def __init__(self, character: Static, target: Static, max_speed: float, radius: float) -> None:
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed
        self.satisfaction_radius = radius

    # The time to target constant.
    timeToTarget: float = 0.25

    def getSteering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Get the direction to the target.
        result.velocity = self.target.position - self.character.position

        if in_radius(result.velocity, self.satisfaction_radius):
            result.velocity = Vector2(0, 0)
            return result

        # If we are outside the satisfaction radius, calculate the target speed.
        result.velocity /= self.timeToTarget

        # If the target speed is greater than the max speed, then clip it.
        if magnitude(result.velocity) > self.max_speed:
            result.velocity = normalize(result.velocity) * self.max_speed

        self.character.orientation = new_orientation(self.character.orientation, result.velocity)

        result.rotation = 0
        return result
    
class KinematicWander:
    def __init__(self, character: Static, max_speed: float, max_rotation: float = 0):
        self.character: Static = character
        self.max_speed: float = max_speed
        self.max_rotation: float = max_rotation

    def get_steering(self) -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        steering.velocity = Vector2(1, 0)
        steering.velocity = rotate_vector(steering.velocity, self.character.orientation)
        steering.velocity *= self.max_speed

        steering.rotation = (random.random() * 2 - 1) * self.max_rotation

        return steering

