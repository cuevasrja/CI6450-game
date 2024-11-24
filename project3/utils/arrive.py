from utils.trigonometry import magnitude, normalize
from pygame import Vector2
from utils.steering_output import SteeringOutput
from utils.kinematic import Kinematic

class Arrive:
    """
    ### Description
    A class to represent an arrive behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to arrive.
    - `max_acceleration` : float : The maximum acceleration of the character.
    - `max_speed` : float : The maximum speed of the character.
    - `target_radius` : float : The radius to stop the character.
    - `slow_radius` : float : The radius to start slowing down the character.
    - `time_to_target` : float : The time to target. (default 0.1)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to arrive at the target.
    """
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_speed: float, target_radius: float, slow_radius: float, time_to_target: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.max_acceleration: float = max_acceleration
        self.max_speed: float = max_speed
        self.target_radius: float = target_radius
        self.slow_radius: float = slow_radius
        self.time_to_target: float = time_to_target

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # Calculate the direction to the target and its magnitude
        direction: Vector2 = self.target.position - self.character.position
        distance: float = magnitude(direction)

        # If the character is inside the target radius, stop
        if distance < self.target_radius:
            steering.linear = Vector2(0, 0)
            return steering

        target_speed: float
        if distance > self.slow_radius: # If the character is outside the slow radius, move at maximum speed
            target_speed = self.max_speed
        else: # Otherwise calculate a scaled speed
            target_speed = self.max_speed * distance / self.slow_radius

        # The target velocity combines speed and direction
        target_velocity: Vector2 = normalize(direction) * target_speed

        # Acceleration tries to get to the target velocity
        steering.linear = target_velocity - self.character.velocity
        steering.linear /= self.time_to_target

        # Check if the acceleration is too great
        if magnitude(steering.linear) > self.max_acceleration:
            steering.linear = normalize(steering.linear) * self.max_acceleration

        # Output the steering with no angular acceleration
        steering.angular = 0
        return steering