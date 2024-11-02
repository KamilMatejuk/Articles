import networkx as nx
import numpy as np

from utils import draw, ORANGE, GREY


def get_nodes(graph: nx.Graph) -> tuple[np.ndarray, dict]:
    n = len(graph.nodes())
    # calculate angles and distances in radial coordinates
    t = np.linspace(0, 2 * np.pi, n)
    # convert to cartesian coordinates
    x = np.cos(t)
    y = np.sin(t)
    points = np.vstack([x, y]).T
    return points, dict(s=4, color=ORANGE)


def get_edges(graph: nx.Graph) -> list[tuple[int, int, dict]]:
    return [(e1, e2, dict(color=GREY)) for e1, e2 in graph.edges()]


if __name__ == '__main__':
    draw('circle.png', get_nodes, get_edges)
