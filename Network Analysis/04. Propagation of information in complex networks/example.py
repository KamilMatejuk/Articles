import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from simulator import State
from visualisator import Visualisator


def position_n_circle(n: int):
    tau = np.linspace(-np.pi, np.pi, n+1)[:-1]
    points = np.array([np.cos(tau), np.sin(tau)]).T
    return points


def generate_graph() -> nx.Graph:
    g = nx.Graph()
    central_node = 'A'
    outer_nodes = ['B', 'C', 'D', 'E', 'F']
    for outer_node in outer_nodes:
        g.add_edge(central_node, outer_node)
    g.add_edge('B', 'C')
    g.add_edge('B', 'F')
    g.add_edge('D', 'E')
    g.nodes[central_node]['state'] = State.SUSCEPTIBLE
    g.nodes['B']['state'] = State.INFECTED
    g.nodes['C']['state'] = State.INFECTED
    g.nodes['D']['state'] = State.SUSCEPTIBLE
    g.nodes['E']['state'] = State.INFECTED
    g.nodes['F']['state'] = State.SUSCEPTIBLE
    return g


def show_both_graphs(g1: nx.Graph, g2: nx.Graph, filename: str):
    positions = np.concatenate((np.array([[0, 0]]), position_n_circle(len(g1.nodes) - 1)), axis=0)
    fig = plt.figure(figsize=(8, 3))
    gs = fig.add_gridspec(1, 3, width_ratios=[5, 2, 5])
    ax1 = fig.add_subplot(gs[0])
    Visualisator.generate_graph(ax1, g1, positions, node_kwargs=dict(s=1000), labels=g1.nodes.keys())
    ax2 = fig.add_subplot(gs[1])
    Visualisator.draw_arrow(ax2)
    ax3 = fig.add_subplot(gs[2])
    Visualisator.generate_graph(ax3, g2, positions, node_kwargs=dict(s=1000), labels=g2.nodes.keys())
    padding = 0.25
    for ax in [ax1, ax3]:
        ax.set_xlim(-1 - padding, 1 + padding)
        ax.set_ylim(-1 - padding, 1 + padding)
    fig.tight_layout()
    plt.savefig(filename)


if __name__ == '__main__':
    graph = generate_graph()
    new_graph = graph.copy()
    new_graph.nodes['A']['state'] = State.INFECTED
    show_both_graphs(graph, new_graph, 'example.png')
