from pygame import Vector2
from utils.physics import SteeringOutput
from utils.seek import Seek

class Path:
    def get_param(self, position: Vector2, current_param: float) -> float:
        pass

    def get_position(self, param: float) -> Vector2:
        pass

class FollowPath(Seek):
    def __init__(self, path: Path, path_ofset: float, current_param: float, **kwargs):
        super().__init__(**kwargs)
        self.path: Path = path
        self.path_offset: float = path_ofset
        self.current_param: float = current_param

    def get_steering(self) -> SteeringOutput:
        current_param: float = self.path.get_param(self.character.position, self.current_param)

        target_param: float = current_param + self.path_offset

        target_position: Vector2 = self.path.get_position(target_param)

        return super().get_steering()