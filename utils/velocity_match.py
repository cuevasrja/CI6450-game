from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import magnitude, normalize

class VelocityMatch:
    """
    ### Description
    A class to represent a velocity match behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to match.
    - `maxAcceleration` : float : The maximum acceleration of the character.
    - `timeToTarget` : float : The time to target. (default 0.1)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to match the target velocity.
    """
    def __init__(self, character: Kinematic, target: Kinematic, maxAcceleration: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.maxAcceleration: float = maxAcceleration
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # The direction is set to the target velocity.
        steering.linear = self.target.velocity
        # The direction is normalized and multiplied by the maximum acceleration.
        steering.linear /= self.timeToTarget

        # Check if the acceleration is too great
        if magnitude(steering.linear) > self.maxAcceleration:
            steering.linear = normalize(steering.linear) * self.maxAcceleration

        # The orientation is set to the angle of the linear direction.
        steering.angular = 0
        return steering