from typing import List
from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import magnitude, normalize

class Separation:
    """
    ### Description
    A class to represent a separation behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `targets` : List[Kinematic] : The targets to avoid.
    - `maxAcceleration` : float : The maximum acceleration of the character.
    - `threshold` : float : The threshold to consider the target.
    - `decayCoefficient` : float : The decay coefficient of the separation.
    - `timeToTarget` : float : The time to target.

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to avoid the targets
    """
    def __init__(self, character: Kinematic, targets: List[Kinematic], player: Kinematic, maxAcceleration: float, threshold: float, decayCoefficient: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.targets: List[Kinematic] = targets
        self.player: Kinematic = player
        self.maxAcceleration: float = maxAcceleration
        self.threshold: float = threshold
        self.decayCoefficient: float = decayCoefficient
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()
        # Use Velocity Mathc behavior to match the player velocity
        steering.linear = self.player.velocity
        steering.linear /= self.timeToTarget

        if magnitude(steering.linear) > self.maxAcceleration:
            steering.linear = normalize(steering.linear) * self.maxAcceleration

        steering.angular = 0

        # Calculate the separation for each target
        for target in self.targets:
            # Check if the target is close
            direction: Vector2 = target.position - self.character.position
            distance: float = direction.length()

            # If the target is close, calculate the separation
            if distance < self.threshold:
                # Calculate the strength of the separation with the decay coefficient
                strength: float = min(self.decayCoefficient / (distance ** 2) if distance != 0 else 0, self.maxAcceleration)
                # Calculate the direction of the separation
                direction = normalize(direction)
                # Add the separation to the steering
                steering.linear += direction * strength

        return steering
