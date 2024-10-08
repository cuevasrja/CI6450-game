from pygame import Vector2
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2, magnitude

class LookWhereYoureGoing(Align):
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def get_steering(self) -> SteeringOutput:
        velocity: Vector2 = self.target.velocity

        if magnitude(velocity) == 0:
            return SteeringOutput()
        
        self.character.orientation = atan2(velocity.x, velocity.y)

        return super().get_steering()