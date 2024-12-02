from pygame import Vector2
from utils.align import Align
from utils.kinematic import Kinematic
from utils.steering_output import SteeringOutput
from utils.trigonometry import atan2, magnitude

class Face(Align):
    """
    ### Description
    A class to represent a face behavior. Extends Align.

    ### Superclass
    Align

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to face.
    - `maxAngularAcceleration` : float : The maximum angular acceleration of the character.
    - `maxRotation` : float : The maximum rotation of the character.
    - `targetRadius` : float : The radius to consider the target as reached.
    - `slowRadius` : float : The radius to start slowing down.
    - `timeToTarget` : float : The time to target. (default 0.1)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to face the target.
    """
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)
        self.target: Kinematic = target.copy()

    def get_steering(self) -> SteeringOutput:
        # Get the direction
        direction: Vector2 = self.target.position - self.character.position

        # Check for a zero direction, and make no change if so
        if magnitude(direction) == 0:
            return SteeringOutput(angular=self.target.angular_velocity)
        
        # Align with the target
        self.target.set_orientation(atan2(direction))

        # Call the align behavior
        align_output: SteeringOutput = super().get_steering()

        return align_output