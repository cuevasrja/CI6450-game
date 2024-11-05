from pygame import Vector2

class KinematicSteeringOutput:
    def __init__(self, velocity: Vector2, rotation: float):
        self.velocity = velocity
        self.rotation = rotation
    