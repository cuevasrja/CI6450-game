from utils.physics import Kinematic, Static, SteeringOutput
from utils.trigonometry import atan2, normalize

class Flee:
    def __init__(self, character: Kinematic, target: Static, max_speed: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        steering.linear = self.character.position - self.target.position
        steering.linear = normalize(steering.linear) * self.max_speed

        self.character.orientation = atan2(steering.linear.x, steering.linear.y)

        steering.angular = 0
        return steering