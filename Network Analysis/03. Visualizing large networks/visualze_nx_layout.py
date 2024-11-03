from typing import Callable
import networkx as nx
import numpy as np

from utils import benchmark, draw, ORANGE, GREY



def get_nodes(graph: nx.Graph, layout: Callable) -> tuple[np.ndarray, dict]:
    points_dict = layout(graph)
    points = np.array([points_dict[n] for n in graph.nodes])
    return points, dict(s=4, color=ORANGE)
def get_nodes_circular(graph: nx.Graph) -> tuple[np.ndarray, dict]:     return get_nodes(graph, nx.circular_layout)
def get_nodes_random(graph: nx.Graph) -> tuple[np.ndarray, dict]:       return get_nodes(graph, nx.random_layout)
def get_nodes_shell(graph: nx.Graph) -> tuple[np.ndarray, dict]:        return get_nodes(graph, nx.shell_layout)
def get_nodes_spring(graph: nx.Graph) -> tuple[np.ndarray, dict]:       return get_nodes(graph, nx.spring_layout)
def get_nodes_spectral(graph: nx.Graph) -> tuple[np.ndarray, dict]:     return get_nodes(graph, nx.spectral_layout)
def get_nodes_kamada_kawai(graph: nx.Graph) -> tuple[np.ndarray, dict]: return get_nodes(graph, nx.kamada_kawai_layout)


def get_edges(graph: nx.Graph) -> list[tuple[int, int, dict]]:
    return [(e1, e2, dict(color=GREY)) for e1, e2 in graph.edges()]


if __name__ == '__main__':
    for get_nodes_function in [
        get_nodes_circular,
        get_nodes_random,
        get_nodes_shell,
        get_nodes_spring,
        get_nodes_spectral,
        # get_nodes_kamada_kawai,
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        # draw(f'nx_{img_label}.png', get_nodes_function, get_edges)
        benchmark(5, f'nx_{img_label}.png', get_nodes_function, get_edges)
