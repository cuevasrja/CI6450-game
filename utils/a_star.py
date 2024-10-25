from typing import List
from utils.graph import Graph, Node, reconstruct_path

def heuristic(node: Node, end: Node) -> float:
    return node.coords.distance_to(end.coords)

def a_star(graph: Graph, start: Node, end: Node) -> List[Node]:
    open_set: list = []
    closed_set: list = []
    came_from: dict = {}
    g_score: dict = {}
    f_score: dict = {}

    for node in graph.get_nodes():
        g_score[node] = float('inf')
        f_score[node] = float('inf')
    g_score[start] = 0
    f_score[start] = heuristic(start, end)
    open_set.append(start)

    while open_set:
        current: Node = min(open_set, key=lambda node: f_score[node])
        if current == end:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        closed_set.append(current)
        for connection in graph.get_connections(current):
            neighbor: Node = connection.get_other_node(current)
            if neighbor in closed_set:
                continue
            tentative_g_score: float = g_score[current] + connection.get_cost()
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
    return []