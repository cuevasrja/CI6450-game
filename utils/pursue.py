from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput
from utils.seek import Seek
from utils.trigonometry import atan2, magnitude, normalize

class Pursue(Seek):
    """
    ### Description
    A class to represent a pursue behavior. Extends Seek.

    ### Superclass
    Seek

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to pursue.
    - `max_speed` : float : The maximum speed of the character.
    - `max_prediction` : float : The maximum prediction of the target.

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to pursue the target.
    """
    def __init__(self, character: Kinematic, target: Kinematic, max_speed: float, max_prediction: float):
        super().__init__(character, target, max_speed)
        self.max_prediction: float = max_prediction
        self.pursue_target: Kinematic = target
    
    def get_steering(self) -> SteeringOutput:
        # The direction is calculated.
        direction: Vector2 = self.pursue_target.position - self.character.position
        # The distance is calculated.
        distance: float = magnitude(direction)
        # The speed is calculated.
        speed: float = magnitude(self.character.velocity)

        prediction: float
        # If the speed is less than the distance divided by the maximum prediction, the prediction is set to the maximum prediction.
        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        # Otherwise, the prediction is set to the distance divided by the speed.
        else:
            prediction = distance / speed

        # The target position is set to the target position plus the target velocity multiplied by the prediction.
        self.target.position += self.pursue_target.velocity * prediction
       
       # The steering is calculated using the Seek superclass.
        return super().get_steering()