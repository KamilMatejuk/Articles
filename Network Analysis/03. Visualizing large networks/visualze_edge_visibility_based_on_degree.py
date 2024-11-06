from typing import Callable
import networkx as nx
import numpy as np

from utils import benchmark, draw, apply_alpha_based_on_degree, GREY

from visualze_basic import get_nodes_grid, get_nodes_circle, get_nodes_spiral
from visualze_nx_layout import get_nodes_spring


def get_edges(graph: nx.Graph) -> list[tuple[int, int, dict]]:
    degrees = [(graph.degree(e1) + graph.degree(e2))/2 for e1, e2 in graph.edges()]
    degrees = [(d-min(degrees)) / (max(degrees)-min(degrees)) for d in degrees]
    degrees = [d**4 for d in degrees]
    edges = []
    for (e1, e2), d in zip(graph.edges(), degrees):
        color = apply_alpha_based_on_degree(GREY, d, min(degrees), max(degrees))
        edges.append((e1, e2, dict(color=color)))
    return edges


if __name__ == '__main__':
    for get_nodes_function in [
        get_nodes_grid,
        get_nodes_circle,
        get_nodes_spiral,
        get_nodes_spring,
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        draw(f'edge_visibility_based_on_degree_pow_{img_label}.png', get_nodes_function, get_edges)
