from a_star import Heuristic
from utils.node import TileNode

class EuclideanHeuristic(Heuristic):
    """
    ### Description
    An implementation of the Euclidean heuristic for the A* algorithm.

    ### Methods
    - `estimate_between(from_node: TileNode, to_node: TileNode) -> float`: Returns the Euclidean distance between two nodes.
    """
    def estimate_between(self, from_node: TileNode, to_node: TileNode) -> float:
        from_tile: TileNode = from_node
        to_tile: TileNode = to_node
        if isinstance(from_node, TileNode) and isinstance(to_node, TileNode):
            return ((from_tile.x - to_tile.x) ** 2 + (from_tile.y - to_tile.y) ** 2) ** 0.5
        return 0