import networkx as nx
import pandas as pd
import numpy as np


def load() -> nx.Graph:
    df = pd.read_csv('network_edges.csv')
    g = nx.Graph()
    for i, row in df.iterrows():
        g.add_edge(row['Person A'], row['Person B'])
        # if i == 2000: break
    print('INFO', len(g.nodes), 'nodes and', len(g.edges), 'edges')
    return g


def get_node_rank(graph: nx.Graph, node: str):
    if node == "me":
        return 1
    if node in graph.neighbors("me"):
        return 2
    return 3


def get_circular_positions(radius: float, n: int) -> dict[str, tuple[float, float]]:
    # calculate angles and distances in radial coordinates
    t = np.linspace(0, 2 * np.pi, n)
    # convert to cartesian coordinates
    x = np.cos(t) * radius
    y = np.sin(t) * radius
    return np.vstack([x, y]).T


def value_01_to_alpha(value: float, min_value: int = 0, max_value: int = 255) -> float:
    alpha = min_value + value * (max_value - min_value)
    alpha = int(min(max(alpha, min_value), max_value))
    return f'{alpha:02x}'


def calculate_node_sizes_based_on_degree(graph: nx.Graph) -> dict:
    degrees = {n: d for n, d in graph.degree}
    min_degree = min(degrees.values())
    max_degree = max(degrees.values())
    degrees_01 = {n: (d - min_degree) / (max_degree - min_degree) for n, d in degrees.items()}
    return degrees_01


def calculate_edge_alphas_based_on_degree(graph: nx.Graph, nodes_2, nodes_3):
    def weighted_degree(e1, e2):
        d1 = graph.degree(e1)
        d2 = graph.degree(e2)
        if e1 in nodes_2: w1 = len(nodes_2)
        else: w1 = len(nodes_3)
        if e2 in nodes_2: w2 = len(nodes_2)
        else: w2 = len(nodes_3)
        return d1 * w1 + d2 * w2
    edge_degrees = {(e1, e2): weighted_degree(e1, e2) for e1, e2 in graph.edges}
    degrees_map = {n: d ** 0.25 for n, d in edge_degrees.items()}
    min_degree = min(degrees_map.values())
    max_degree = max(degrees_map.values())
    degrees_01 = {n: (d - min_degree) / (max_degree - min_degree) for n, d in degrees_map.items()}
    edge_alpha = {n: value_01_to_alpha(d, 0, 60) for n, d in degrees_01.items()}
    return edge_alpha
