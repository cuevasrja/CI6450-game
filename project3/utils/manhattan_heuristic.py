from utils.a_star import Heuristic
from utils.node import TileNode

class ManhattanHeuristic(Heuristic):
    """
    ### Description
    A class to represent the Manhattan heuristic.

    ### Methods
    - `estimate_between(from_node: TileNode, to_node: TileNode) -> float`
        Returns the Manhattan distance between `from_node` and `to_node`.
    """
    def estimate_between(self, from_node: TileNode, to_node: TileNode) -> float:
        if isinstance(from_node, TileNode) and isinstance(to_node, TileNode):
            return abs(from_node.x - to_node.x) + abs(from_node.y - to_node.y)
        return 0
