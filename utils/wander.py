import math
import random
from pygame import Vector2
from utils.face import Face
from utils.physics import Kinematic, SteeringOutput

def random_binomial() -> float:
    return random.uniform(-1, 1)

class Wander(Face):
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, wanderOffset: float, wanderRadius: float, wanderRate: float, wanderOrientation: float, maxAcceleration: float):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius)
        self.wanderOffset: float = wanderOffset
        self.wanderRadius: float = wanderRadius
        self.wanderRate: float = wanderRate
        self.wanderOrientation: float = wanderOrientation
        self.maxAcceleration: float = maxAcceleration

    def get_steering(self) -> SteeringOutput:
        self.wanderOrientation += random_binomial() * self.wanderRate

        targetOrientation: float = self.wanderOrientation + self.character.orientation

        target: Vector2 = Vector2(self.character.position.x + self.wanderOffset * math.cos(self.character.orientation), self.character.position.y + self.wanderOffset * math.sin(self.character.orientation))
        
        target.x += self.wanderRadius * math.cos(targetOrientation)
        target.y += self.wanderRadius * math.sin(targetOrientation)

        result: SteeringOutput = super().get_steering()

        result.linear = Vector2(self.maxAcceleration * math.cos(self.character.orientation), self.maxAcceleration * math.sin(self.character.orientation))

        return result