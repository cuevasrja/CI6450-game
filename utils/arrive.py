from typing import Tuple
from utils.physics import Kinematic, SteeringOutput
from utils.trigonometry import magnitude, normalize
from pygame import Vector2

class Arrive:
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_speed: float, target_radius: float, slow_radius: float, time_to_target: float = 0.1):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.max_acceleration: float = max_acceleration
        self.max_speed: float = max_speed
        self.target_radius: float = target_radius
        self.slow_radius: float = slow_radius
        self.time_to_target: float = time_to_target

    def get_steering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()

        direction: Vector2 = self.target.position - self.character.position
        distance: float = magnitude(direction)

        if distance < self.target_radius:
            steering.linear = Vector2(0, 0)
            return steering

        target_speed: float
        if distance > self.slow_radius:
            target_speed = self.max_speed
        else:
            target_speed = self.max_speed * distance / self.slow_radius

        target_velocity: Vector2 = normalize(direction) * target_speed

        steering.linear = target_velocity - self.character.velocity
        steering.linear = steering.linear / self.time_to_target

        if magnitude(steering.linear) > self.max_acceleration:
            steering.linear = normalize(steering.linear) * self.max_acceleration

        steering.angular = 0
        return steering