from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import magnitude, normalize

class VelocityMatch:
    def __init__(self, character: Kinematic, target: Kinematic, maxAcceleration: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.maxAcceleration: float = maxAcceleration
        self.timeToTarget: float = timeToTarget

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        steering.linear = self.target.velocity - self.character.velocity
        steering.linear /= self.timeToTarget

        print(steering.linear)
        if magnitude(steering.linear) > self.maxAcceleration:
            steering.linear = normalize(steering.linear) * self.maxAcceleration

        steering.angular = 0
        return steering