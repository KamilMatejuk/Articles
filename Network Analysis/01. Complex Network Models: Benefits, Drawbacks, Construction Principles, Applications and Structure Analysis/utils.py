import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


FIGSIZE_GROUP = (20, 4)
FIGSIZE_ONE = (5, 4)
COLOR = '#FF3C00'


def plot_repr(graphs: list[nx.Graph], labels: list[str]):
    fig, axes = plt.subplots(1, len(graphs), figsize=(FIGSIZE_ONE if len(graphs) == 1 else FIGSIZE_GROUP))
    if len(graphs) == 1: axes = [axes]
    for g, ax, l in zip(graphs, axes, labels):
        scale = ((8 - np.log(len(g.nodes))) / 5)
        scale = max(0, min(1, scale))
        nx.draw_kamada_kawai(g, node_size=50*scale, alpha=0.7, width=scale, node_color=COLOR, edge_color='grey', ax=ax)
        ax.set_title(l)
    plt.show()


def plot_distribution(values: list[list[float | int]], labels: list[str]):
    fig, axes = plt.subplots(1, len(values), figsize=(FIGSIZE_ONE if len(values) == 1 else FIGSIZE_GROUP))
    if len(values) == 1: axes = [axes]
    for vals, ax, l in zip(values, axes, labels):
        if isinstance(vals[0], int):
            bins = range(min(vals), max(vals) + 2)
            width = 0.9
        else:
            bins = 25
            width = 0.9 * (max(vals) - min(vals)) / bins

        hist, bins = np.histogram(vals, bins=bins, density=False)
        ax.bar(bins[:-1], hist, width=width, color=COLOR)
        ax.set_ylabel('Frequency')
        ax.set_title(l)
    plt.show()


def plot_degree_distribution(graphs: list[nx.Graph], labels: list[str]):
    degrees = [[g.degree(node) for node in g.nodes()] for g in graphs]
    plot_distribution(degrees, labels)


def plot_betweenness_centrality_distribution(graphs: list[nx.Graph], labels: list[str]):
    centrs = [list(nx.betweenness_centrality(g).values()) for g in graphs]
    plot_distribution(centrs, labels)


def plot_closeness_centrality_distribution(graphs: list[nx.Graph], labels: list[str]):
    centrs = [list(nx.closeness_centrality(g).values()) for g in graphs]
    plot_distribution(centrs, labels)


def plot_shortest_path_distribution(graphs: list[nx.Graph], labels: list[str]):
    labels = labels.copy()
    path_lens = []
    for i, g in enumerate(graphs):
        pl = []
        for u in g.nodes():
            for v in g.nodes():
                if u == v: continue
                pl.append(nx.shortest_path_length(g, u, v))
        path_lens.append(pl)
        n = len(g.nodes())
        avg = sum(pl) / ((n-1) * n)
        # print(f'Average shortest path length {avg:.2f}')
        # print(f'Maximum shortest path length {max(pl):.2f}')
        labels[i] = f'{labels[i]}\navg {avg:.2f} max {max(pl):.0f}'.strip()
    plot_distribution(path_lens, labels)


def plot_all(graphs: list[nx.Graph], labels: list[str]):
    plot_repr(graphs, labels)
    plot_degree_distribution(graphs, labels)
    plot_betweenness_centrality_distribution(graphs, labels)
    plot_closeness_centrality_distribution(graphs, labels)
    plot_shortest_path_distribution(graphs, labels)
