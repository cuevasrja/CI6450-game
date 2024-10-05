from typing import List
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2

class LookWhereYoureGoing(Align):
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def get_steering(self) -> SteeringOutput:
        velocity: List[float] = self.character.velocity

        if velocity == [0, 0]:
            return SteeringOutput()
        
        self.target.orientation = atan2(-velocity[0], velocity[1])

        return super().get_steering()