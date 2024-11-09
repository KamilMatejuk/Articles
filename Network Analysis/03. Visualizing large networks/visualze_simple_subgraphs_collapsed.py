from typing import Callable
import networkx as nx
import numpy as np
import random

from utils import draw, map01, ORANGE, GREEN
from visualze_edge_visibility_based_on_degree import get_edges

from visualze_basic import get_nodes_grid as get_node_pos_grid
from visualze_basic import get_nodes_circle as get_node_pos_circle
from visualze_basic import get_nodes_spiral as get_node_pos_spiral
from visualze_nx_layout import get_nodes_spring as get_node_pos_spring
from visualze_nx_layout import get_nodes_kamada_kawai as get_node_pos_kamada_kawai


def edit(graph: nx.Graph) -> list[str]:
    nx.set_node_attributes(graph, 0, 'community')
    nodes_to_remove = set()
    for node, degree in graph.degree():
        if degree != 1: continue
        anchor = next(graph.neighbors(node))
        graph.nodes[anchor]['community'] += 1
        nodes_to_remove.add(node)
    graph.remove_nodes_from(nodes_to_remove)
    print(f'Collapsed {len(nodes_to_remove)} nodes into communities')
    # randomize node order
    nodes = list(graph.nodes)
    random.shuffle(nodes)
    graph._node = {n: graph.nodes[n] for n in nodes}
    return graph


def get_nodes(graph: nx.Graph, get_pos: Callable) -> tuple[np.ndarray, dict]:
    pos, kwargs = get_pos(graph)
    communities = map01(data['community'] for _, data in graph.nodes(data=True))
    degrees = map01(graph.degree(n) for n in graph.nodes)
    sizes = [1000 * (2*c + d if c > 0 else 5 * d) for c, d in zip(communities, degrees)]
    colors = [f'{ORANGE}88' if c > 0 else f'{GREEN}88' for c in communities]
    kwargs['s'] = sizes
    kwargs['color'] = colors
    return pos, kwargs
def get_nodes_grid(graph: nx.Graph) -> tuple[np.ndarray, dict]:         return get_nodes(graph, get_node_pos_grid)
def get_nodes_circle(graph: nx.Graph) -> tuple[np.ndarray, dict]:       return get_nodes(graph, get_node_pos_circle)
def get_nodes_spiral(graph: nx.Graph) -> tuple[np.ndarray, dict]:       return get_nodes(graph, get_node_pos_spiral)
def get_nodes_spring(graph: nx.Graph) -> tuple[np.ndarray, dict]:       return get_nodes(graph, get_node_pos_spring)
def get_nodes_kamada_kawai(graph: nx.Graph) -> tuple[np.ndarray, dict]: return get_nodes(graph, get_node_pos_kamada_kawai)


if __name__ == '__main__':
    for get_nodes_function in [
        get_nodes_grid,
        get_nodes_circle,
        get_nodes_spiral,
        get_nodes_spring,
        get_nodes_kamada_kawai
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        draw(f'simple_subgraphs_collapsed_deg_{img_label}.png', get_nodes_function, get_edges, edit)
