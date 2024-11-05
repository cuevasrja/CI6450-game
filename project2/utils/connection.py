from utils.node import Node

class Connection:
    """
    ### Description
    A connection between two nodes in a graph.

    ### Attributes
    - `from_node`: The node where the connection starts.
    - `to_node`: The node where the connection ends.
    - `_cost`: The cost of traversing the connection.
    """
    def __init__(self, from_node: Node, to_node: Node, cost: float):
        self.from_node = from_node
        self.to_node = to_node
        self._cost = cost

    def get_cost(self) -> float:
        return self._cost
    
    def get_from_node(self) -> Node:
        return self.from_node
    
    def get_to_node(self) -> Node:
        return self.to_node
