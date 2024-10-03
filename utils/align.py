from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import map_to_range

class Align:
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.maxAngularAcceleration: float = maxAngularAcceleration
        self.maxRotation: float = maxRotation
        self.targetRadius: float = targetRadius
        self.slowRadius: float = slowRadius
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        rotation: float = self.target.orientation - self.character.orientation
        rotation = map_to_range(rotation)

        rotationSize: float = abs(rotation)

        if rotationSize < self.targetRadius:
            steering.angular = 0
            return steering

        targetRotation: float
        if rotationSize > self.slowRadius:
            targetRotation = self.maxRotation
        else:
            targetRotation = self.maxRotation * rotationSize / self.slowRadius

        targetRotation *= rotation / rotationSize

        steering.angular = targetRotation - self.character.angular_velocity
        steering.angular /= self.timeToTarget

        if abs(steering.angular) > self.maxAngularAcceleration:
            steering.angular = self.maxAngularAcceleration * steering.angular / abs(steering.angular)

        steering.linear = (0, 0)
        return steering