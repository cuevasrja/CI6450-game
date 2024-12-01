from pygame import Vector2
from utils.kinematic import Kinematic
from utils.steering_output import SteeringOutput
from utils.trigonometry import map_to_range

class Align:
    """
    ### Description
    A class to represent an align behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to align.
    - `maxAngularAcceleration` : float : The maximum angular acceleration of the character.
    - `maxRotation` : float : The maximum rotation of the character.
    - `targetRadius` : float : The radius to consider the target as reached.
    - `slowRadius` : float : The radius to start slowing down.
    - `timeToTarget` : float : The time to target. (default 0.1)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to align the character with the target.
    """
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.maxAngularAcceleration: float = maxAngularAcceleration
        self.maxRotation: float = maxRotation
        self.targetRadius: float = targetRadius
        self.slowRadius: float = slowRadius
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # Get the rotation direction
        rotation: float = self.target.orientation - self.character.orientation
        # Map the result to the (-pi, pi) interval
        rotation = map_to_range(rotation)

        # Get the absolute value of the rotation
        rotationSize: float = abs(rotation)

        # Check if we are there, return no steering
        if rotationSize < self.targetRadius:
            steering.angular = 0
            return steering

        targetRotation: float
        if rotationSize > self.slowRadius: # If we are outside the slowRadius, then use maximum rotation
            targetRotation = self.maxRotation
        else: # Otherwise calculate a scaled rotation
            targetRotation = self.maxRotation * rotationSize / self.slowRadius

        # The final target rotation combines speed and direction
        targetRotation *= rotation / rotationSize

        # Acceleration tries to get to the target rotation
        steering.angular = targetRotation - self.character.angular_velocity
        steering.angular /= self.timeToTarget

        # Check if the acceleration is too great
        if abs(steering.angular) > self.maxAngularAcceleration:
            steering.angular = self.maxAngularAcceleration * steering.angular / abs(steering.angular)

        # Output the steering with no linear velocity
        steering.linear = Vector2(0, 0)
        return steering
    