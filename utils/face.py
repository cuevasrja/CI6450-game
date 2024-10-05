from typing import List
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2


class Face(Align):
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)
        self.target: Kinematic = target

    def get_steering(self, explicit_target: Kinematic) -> SteeringOutput:
        direction: List[float] = [self.target.position[0] - self.character.position[0], self.target.position[1] - self.character.position[1]]

        if direction == [0, 0]:
            return self.target
        
        super().target = explicit_target
        super().target.orientation = atan2(-direction[0], direction[1])

        return super().get_steering()