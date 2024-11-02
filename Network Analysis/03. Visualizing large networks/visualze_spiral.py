import networkx as nx
import numpy as np

from utils import draw, ORANGE, GREY


def get_nodes(graph: nx.Graph) -> tuple[np.ndarray, dict]:
    turns = 15
    n = len(graph.nodes())
    # calculate angles and distances in radial coordinates
    t = np.linspace(0, turns * 2 * np.pi, n)
    r = np.linspace(0, 1, n)
    # convert to cartesian coordinates
    x = r * np.cos(t)
    y = r * np.sin(t)
    points = np.vstack([x, y]).T
    return points, dict(s=4, color=ORANGE)


def get_edges(graph: nx.Graph) -> list[tuple[int, int, dict]]:
    return [(e1, e2, dict(color=GREY)) for e1, e2 in graph.edges()]


if __name__ == '__main__':
    draw('spiral.png', get_nodes, get_edges)
