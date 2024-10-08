from pygame import Vector2
from utils.align import Align
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import atan2, magnitude, normalize

class LookWhereYoureGoing(Align):
    max_speed: float = 300

    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, timeToTarget: float = 0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    # def get_steering(self) -> SteeringOutput:
    #     velocity: Vector2 = self.character.velocity

    #     if magnitude(velocity) == 0:
    #         return SteeringOutput()
        
    #     self.target.orientation = atan2(velocity.x, velocity.y)

    #     return super().get_steering()

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        steering.linear = self.character.position - self.target.position
        steering.linear = normalize(steering.linear) * self.max_speed

        self.character.orientation = atan2(steering.linear.x, steering.linear.y)

        steering.angular = 0

        velocity: Vector2 = steering.linear

        self.target.orientation = atan2(velocity.x, velocity.y)

        return steering