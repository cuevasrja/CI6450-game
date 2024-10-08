from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput
from utils.seek import Seek
from utils.trigonometry import atan2, magnitude, normalize

class Pursue(Seek):
    def __init__(self, character: Kinematic, target: Kinematic, max_speed: float, max_prediction: float):
        super().__init__(character, target, max_speed)
        self.max_prediction: float = max_prediction
        self.pursue_target: Kinematic = target
    
    def get_steering(self) -> SteeringOutput:
        direction: Vector2 = self.pursue_target.position - self.character.position
        distance: float = magnitude(direction)
        speed: float = magnitude(self.character.velocity)

        prediction: float
        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed

        self.target.position += self.pursue_target.velocity * prediction
       
        return super().get_steering()