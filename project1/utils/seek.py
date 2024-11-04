from typing import Tuple
from utils.physics import Kinematic, Static, SteeringOutput
from utils.trigonometry import atan2, normalize

class Seek:
    """
    ### Description
    A class to represent a seek behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Static : The target to seek.
    - `max_speed` : float : The maximum speed of the character.

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to seek the target.
    """
    def __init__(self, character: Kinematic, target: Static, max_speed: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # The direction is set to the target position minus the character position.
        steering.linear = self.target.position - self.character.position
        # The direction is normalized and multiplied by the maximum speed.
        steering.linear = normalize(steering.linear) * self.max_speed

        # The orientation is set to the angle of the linear direction.
        self.character.orientation = atan2(steering.linear.x, steering.linear.y)

        # The angular is set to 0.
        steering.angular = 0
        return steering
