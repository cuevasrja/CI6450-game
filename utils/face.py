from pygame import Vector2
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2, magnitude

class Face(Align):
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)
        self.target: Kinematic = target

    def get_steering(self) -> SteeringOutput:
        direction: Vector2 = Vector2(self.target.position.x - self.character.position.x, self.target.position.y - self.character.position.y)

        if magnitude(direction) == 0:
            return self.target
        
        self.target = self.target.copy()
        self.target.orientation = atan2(-direction.x, direction.y)

        return super().get_steering()