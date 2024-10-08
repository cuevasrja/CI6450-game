from typing import List

from pygame import Vector2
from utils.physics import Kinematic, SteeringOutput


class CollisionAvoidance:
    def __init__(self, character: Kinematic, targets: List[Kinematic], maxAcceleration: float, radius: float):
        self.character: Kinematic = character
        self.targets: List[Kinematic] = targets
        self.maxAcceleration: float = maxAcceleration
        self.radius: float = radius
        

    def get_steering(self) -> SteeringOutput:
        shortest_time: float = float('inf')
        first_target: Kinematic = None
        first_min_separation: float = 0
        first_distance: float = 0
        first_relative_position: Vector2 = None
        first_relative_velocity: Vector2 = None

        for target in self.targets:
            relative_position: Vector2 = target.position - self.character.position
            relative_velocity: Vector2 = target.velocity - self.character.velocity
            relative_speed: float = relative_velocity.length()
            time_to_collision: float = relative_position.dot(relative_velocity) / (relative_speed ** 2) if relative_speed != 0 else 0

            distance: float = relative_position.length()
            min_separation: float = distance - relative_speed * time_to_collision
            if min_separation > 2 * self.radius:
                continue

            if time_to_collision > 0 and time_to_collision < shortest_time:
                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_distance = distance
                first_relative_position = relative_position
                first_relative_velocity = relative_velocity

        if first_target is None:
            return SteeringOutput()
        
        if first_min_separation <= 0 or first_distance < 2 * self.radius:
            relative_position = first_target.position - self.character.position
        else:
            relative_position = first_relative_position + first_relative_velocity * shortest_time

        relative_position = relative_position.normalize()

        steering: SteeringOutput = SteeringOutput(linear=relative_position * self.maxAcceleration, angular=0)
        return steering

