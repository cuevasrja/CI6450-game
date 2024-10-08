from typing import List
from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import magnitude, normalize

class Separation:
    def __init__(self, character: Kinematic, targets: List[Kinematic], player: Kinematic, maxAcceleration: float, threshold: float, decayCoefficient: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.targets: List[Kinematic] = targets
        self.player: Kinematic = player
        self.maxAcceleration: float = maxAcceleration
        self.threshold: float = threshold
        self.decayCoefficient: float = decayCoefficient
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()
        steering.linear = self.player.velocity
        steering.linear /= self.timeToTarget

        if magnitude(steering.linear) > self.maxAcceleration:
            steering.linear = normalize(steering.linear) * self.maxAcceleration

        steering.angular = 0

        for target in self.targets:
            direction: Vector2 = self.character.position - target.position
            distance: float = direction.length()

            if distance < self.threshold:
                strength: float = min(self.decayCoefficient / (distance ** 2) if distance != 0 else 0, self.maxAcceleration)
                direction = normalize(direction)
                steering.linear += direction * strength

        return steering
