from pygame import Vector2
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2, magnitude, normalize

class LookWhereYoureGoing(Align):
    """
    ### Description
    A class to represent a look where you're going behavior. Extends Align.

    ### Superclass
    Align

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to align.
    - `maxAngularAcceleration` : float : The maximum angular acceleration of the character.
    - `maxRotation` : float : The maximum rotation of the character.
    - `targetRadius` : float : The radius to consider the target as reached.
    - `slowRadius` : float : The radius to start slowing down.
    - `maxSpeed` : float : The maximum speed of the character.
    - `timeToTarget` : float : The time to target. (default 0.1)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to align the character with the velocity.
    """

    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, maxSpeed: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)
        self.maxSpeed: float = maxSpeed


    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        # Calculate the target to delegate the align behavior
        steering.linear = self.character.position - self.target.position
        # Normalize the direction
        steering.linear = normalize(steering.linear) * self.maxSpeed

        # If the character is stopped, return no steering
        if magnitude(steering.linear) == 0:
            return steering

        # Align with the target
        self.character.orientation = atan2(steering.linear.x, steering.linear.y)

        # Set the angular velocity to 0
        steering.angular = 0

        velocity: Vector2 = steering.linear

        # Set the orientation to the velocity
        self.target.orientation = atan2(velocity.x, velocity.y)

        return steering