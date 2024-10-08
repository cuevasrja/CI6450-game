from utils.physics import Kinematic, Static, SteeringOutput
from utils.trigonometry import atan2, normalize

class Flee:
    """
    ### Description
    A class to represent a flee behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Static : The target to flee.
    - `max_speed` : float : The maximum speed of the character.

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to flee the target.
    """
    def __init__(self, character: Kinematic, target: Static, max_speed: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # The direction is reversed.
        steering.linear = self.character.position - self.target.position
        # The direction is normalized and multiplied by the maximum speed.
        steering.linear = normalize(steering.linear) * self.max_speed

        # The orientation is set to the angle of the linear direction.
        self.character.orientation = atan2(steering.linear.x, steering.linear.y)

        # The angular is set to 0.
        steering.angular = 0
        return steering