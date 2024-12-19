
import tqdm
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from utils import load, get_node_rank, get_circular_positions, calculate_node_sizes_based_on_degree, calculate_edge_alphas_based_on_degree

random.seed(12345)

COLOR_RANK_1 = '#E4572E'
COLOR_RANK_2 = '#6290C3'
COLOR_RANK_3 = '#3BBA6C'


def generate(graph: nx.Graph, nodes_2: list[str], nodes_3: list[str], show_level_3: bool, filename: str,
             node_sizes: dict = None, edge_alphas: dict = None):
    plt.figure(figsize=(12, 12))
    
    positions = {'me': (0, 0)}
    
    # me
    x, y = positions['me']
    plt.scatter(x, y, zorder=2, s=50, c=COLOR_RANK_1)
    
    # my connections
    random.shuffle(nodes_2)
    pos = get_circular_positions(0.4, len(nodes_2))
    sizes = [int(100 * node_sizes[n]) for n in nodes_2] if node_sizes else 10
    plt.scatter(pos[:, 0], pos[:, 1], zorder=2, s=sizes, c=COLOR_RANK_2)

    for node, (x, y) in zip(nodes_2, pos):
        positions[node] = (x, y)

    for e1, e2 in tqdm.tqdm(graph.edges):
        if e1 not in positions or e2 not in positions: continue
        coordinates = np.array([positions[e1], positions[e2]])
        if e1 == "me" or e2 == "me":
            color = COLOR_RANK_1 + (edge_alphas[(e1, e2)] if edge_alphas else '55')
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=3, color=color, linewidth=0.5)
        else:
            color = '#999999' + (edge_alphas[(e1, e2)] if edge_alphas else '55')
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color=color, linewidth=0.5)

    # my connections of connections
    if show_level_3:
        nodes_3_sorted_by_nodes_2 = []
        for n2 in nodes_2:
            for n3 in graph.neighbors(n2):
                if n3 not in nodes_3: continue
                if n3 in nodes_3_sorted_by_nodes_2: continue
                if graph.degree(n3) != 1: continue
                nodes_3_sorted_by_nodes_2.append(n3)
        for n3 in nodes_3:
            if n3 in nodes_3_sorted_by_nodes_2: continue
            ri = random.randint(0, len(nodes_3_sorted_by_nodes_2))
            nodes_3_sorted_by_nodes_2 = nodes_3_sorted_by_nodes_2[:ri] + [n3] + nodes_3_sorted_by_nodes_2[ri:]
        pos = get_circular_positions(1.0, len(nodes_3_sorted_by_nodes_2))
        for node, (x, y) in zip(nodes_3_sorted_by_nodes_2, pos):
            positions[node] = (x, y)

        sizes = [int(1000 * node_sizes[n]) for n in nodes_3_sorted_by_nodes_2] if node_sizes else 10
        plt.scatter(pos[:, 0], pos[:, 1], zorder=2, s=sizes, c=COLOR_RANK_3)

        # edges
        for e1, e2 in tqdm.tqdm(graph.edges):
            if e1 not in positions or e2 not in positions: continue
            coordinates = np.array([positions[e1], positions[e2]])
            if e1 not in nodes_3 and e2 not in nodes_3: continue
            color = '#999999' + (edge_alphas[(e1, e2)] if edge_alphas else '55')
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color=color, linewidth=0.5)
    
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(filename)


if __name__ == '__main__':
    g = load()
    nodes_2 = [n for n in g.nodes if get_node_rank(g, n) == 2]
    nodes_3 = [n for n in g.nodes if get_node_rank(g, n) == 3]
    # generate(g, nodes_2, nodes_3, False, 'images/visualization_2.png')
    # generate(g, nodes_2, nodes_3, True, 'images/visualization_3.png')
    generate(g, nodes_2, nodes_3, True, 'images/visualization_3_improved2.png',
             node_sizes=calculate_node_sizes_based_on_degree(g),
             edge_alphas=calculate_edge_alphas_based_on_degree(g, nodes_2, nodes_3))
