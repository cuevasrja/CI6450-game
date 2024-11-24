from utils.connection import Connection
from utils.node import Node

class Graph:
    """
    ### Description
    A class to represent a graph.

    ### Attributes
    - `connections`: dict[Node, list[Connection]]
        A dictionary that maps a node to a list of connections.

    ### Methods
    - `add_connection(from_node: Node, to_node: Node, cost: float) -> None`
        Adds a connection from `from_node` to `to_node` with a cost of `cost`.
    - `get_connections(from_node: Node) -> list[Connection]`
        Returns a list of connections from `from_node`.
    """
    def __init__(self):
        self.connections = {}

    def add_connection(self, from_node: Node, to_node: Node, cost: float):
        if from_node not in self.connections:
            self.connections[from_node] = []
        self.connections[from_node].append(Connection(from_node, to_node, cost))

    def get_connections(self, from_node: Node) -> list[Connection]:
        return self.connections.get(from_node, [])