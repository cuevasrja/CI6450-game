from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput
from utils.seek import Seek
from utils.trigonometry import atan2, magnitude, normalize

class Pursue(Seek):
    def __init__(self, character: Kinematic, target: Kinematic, max_speed: float, max_prediction: float):
        super().__init__(character, target, max_speed)
        self.max_prediction: float = max_prediction
        # Override target
        self.target: Kinematic = target
    
    def get_steering(self) -> SteeringOutput:
        direction: Vector2 = Vector2(self.target.position[0] - self.character.position[0], self.target.position[1] - self.character.position[1])
        distance: float = magnitude(direction)
        speed: float = magnitude(self.character.velocity)

        prediction: float
        if speed <= distance / self.max_prediction:
            prediction = self.max_prediction
        else:
            prediction = distance / speed

        super().target = Kinematic()
        super().target.position *= self.target.velocity * prediction
       
        return super().get_steering()