from typing import List
from pygame import Vector2
from utils.physics import Kinematic, Static, SteeringOutput
from utils.seek import Seek
from utils.trigonometry import magnitude

class Path:
    def __init__(self, points: List[Vector2] = Vector2(0,0), cur: int = 0, offset: float = 0):
        self.points: List[Vector2] = points
        self.cur: int = cur
        self.offset: float = offset

    def get_param(self, position: Vector2, current_param: int) -> float:
        if current_param >= len(self.points):
            return current_param
        while current_param < len(self.points) - 1:
            if magnitude(self.points[current_param] - position) < self.offset:
                current_param += 1
            else:
                break
        return current_param

    def get_position(self, param: int) -> Vector2:
        return self.points[param]
    
    def set_param(self, param: int):
        if param < len(self.points):
            self.cur = param
        else:
            self.cur = 0

class FollowPath(Seek):
    def __init__(self, character: Kinematic, target: Static, max_speed: float, path: List[Vector2], path_ofset: float, current_param: int = 0):
        super().__init__(character, target, max_speed)
        self.path: Path = Path(path, current_param, path_ofset)


    def get_steering(self) -> SteeringOutput:
        current_param: float = self.path.get_param(self.character.position, self.path.cur)

        target_param: float = current_param + self.path.cur
        self.path.set_param(target_param)

        target_position: Vector2 = self.path.get_position(self.path.cur)

        self.target = self.target.copy()
        self.target.position = Vector2(target_position.x, target_position.y)

        return super().get_steering()