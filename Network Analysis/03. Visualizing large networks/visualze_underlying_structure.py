import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import json
import os

from utils import Timer, load, ORANGE, GREY

from visualze_edge_visibility_based_on_degree import get_edges
from visualze_nx_layout import get_nodes_kamada_kawai as get_node_pos_kamada_kawai


def save_hist(graph: nx.Graph, filename: str):
    degrees = [d for _, d in graph.degree()]
    plt.figure(figsize=(12, 6))
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2, 2), edgecolor='black')
    plt.xlabel('Degree', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.yscale('log')
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename))


def save_visualization(graph: nx.Graph, filename: str,
        graph_nodes: list[str], graph_nodes_pos: np.ndarray,
        graph_nodes_size: np.ndarray, removed_node_indexes: list[int]):
    plt.figure(figsize=(12, 12))
    mask_p = np.ones(graph_nodes_pos.shape[0], dtype=bool)
    mask_p[removed_node_indexes] = False
    mask_s = np.ones(graph_nodes_size.shape[0], dtype=bool)
    mask_s[removed_node_indexes] = False
    
    plt.scatter(graph_nodes_pos[mask_p, 0],
                graph_nodes_pos[mask_p, 1],
                s=graph_nodes_size[mask_s],
                zorder=2, color=f'{ORANGE}88')

    edges = get_edges(graph)
    with Timer('Edges', {}, len(edges)) as timer:
        for e1, e2, kwargs in edges:
            coordinates = np.array([graph_nodes_pos[graph_nodes.index(e1)], graph_nodes_pos[graph_nodes.index(e2)]])
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, **kwargs)
            timer.step()

    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename))


def simplify(graph: nx.Graph, removed_node_indexes: list[int]) -> tuple[nx.Graph, list[int]]:
    min_degree = min(d for _, d in graph.degree())
    nodes_to_remove = set((i, n) for i, (n, d) in enumerate(graph.degree) if d == min_degree)
    removed_node_indexes += list(x[0] for x in nodes_to_remove)
    graph.remove_nodes_from(x[1] for x in nodes_to_remove)
    print(f'Removed {len(nodes_to_remove)} nodes of degree {min_degree}')
    if len(nodes_to_remove) < 10: return simplify(graph, removed_node_indexes)
    return graph, removed_node_indexes


if __name__ == '__main__':
    G: nx.Graph = load()
    G, _ = simplify(G, [])
    removed_nodes_i = list()

    all_nodes = list(G.nodes)
    nodes, _ = get_node_pos_kamada_kawai(G)
    sizes = np.array([2*d for _, d in G.degree()])

    for iter in range(1, 6):
        print(iter)
        save_hist(G, f'underlying_structure_deghist_{iter}.png')
        save_visualization(G, f'2underlying_structure_graph_{iter}.png',
                           all_nodes, nodes, sizes, removed_nodes_i)
        G, removed_nodes_i = simplify(G, removed_nodes_i)
