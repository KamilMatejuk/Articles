from typing import Callable
import networkx as nx
import numpy as np

from utils import benchmark, draw, apply_alpha_based_on_degree, ORANGE

from visualze_basic import get_nodes_grid as get_node_pos_grid
from visualze_basic import get_nodes_circle as get_node_pos_circle
from visualze_basic import get_nodes_spiral as get_node_pos_spiral
from visualze_nx_layout import get_nodes_spring as get_node_pos_spring
from visualze_edge_visibility_based_on_degree import get_edges

def get_nodes(graph: nx.Graph, get_pos: Callable) -> tuple[np.ndarray, dict]:
    pos, kwargs = get_pos(graph)
    degrees = [graph.degree(n) for n in graph.nodes]
    degrees = [(d-min(degrees)) / (max(degrees)-min(degrees)) for d in degrees]
    degrees = [d**0.2 for d in degrees]
    colors = [apply_alpha_based_on_degree(ORANGE, d, min(degrees), max(degrees)) for d in degrees]
    kwargs['color'] = colors
    return pos, kwargs
def get_nodes_grid(graph: nx.Graph) -> tuple[np.ndarray, dict]:     return get_nodes(graph, get_node_pos_grid)
def get_nodes_circle(graph: nx.Graph) -> tuple[np.ndarray, dict]:   return get_nodes(graph, get_node_pos_circle)
def get_nodes_spiral(graph: nx.Graph) -> tuple[np.ndarray, dict]:   return get_nodes(graph, get_node_pos_spiral)
def get_nodes_spring(graph: nx.Graph) -> tuple[np.ndarray, dict]:   return get_nodes(graph, get_node_pos_spring)


if __name__ == '__main__':
    for get_nodes_function in [
        get_nodes_grid,
        get_nodes_circle,
        get_nodes_spiral,
        get_nodes_spring,
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        draw(f'node_visibility_based_on_degree_{img_label}.png', get_nodes_function, get_edges)
