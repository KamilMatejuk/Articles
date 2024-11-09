from typing import Callable
import networkx as nx
import numpy as np

from utils import draw
from visualze_edge_visibility_based_on_degree import get_edges
from visualze_node_visibility_based_on_degree import get_nodes_grid, get_nodes_circle, get_nodes_spiral, get_nodes_spring


def edit(graph: nx.Graph) -> list[str]:
    sorted_nodes = sorted(graph.nodes, key=lambda x: graph.degree(x), reverse=True)
    graph._node = {n: graph.nodes[n] for n in sorted_nodes}
    return graph


if __name__ == '__main__':
    for get_nodes_function in [
        get_nodes_grid,
        get_nodes_circle,
        get_nodes_spiral,
        get_nodes_spring,
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        draw(f'node_sorted_by_degree_{img_label}.png', get_nodes_function, get_edges, edit)
