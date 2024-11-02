import networkx as nx
import numpy as np

from utils import draw, ORANGE, GREY


def get_nodes(graph: nx.Graph) -> tuple[np.ndarray, dict]:
    n = len(graph.nodes())
    # device equally into rows and cols
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))
    # create equal points for rows and cols
    linspace = lambda items: np.linspace(1/items/3, 1-1/items/3, items)
    x = linspace(cols)
    y = linspace(rows)
    # create grid of points
    xv, yv = np.meshgrid(x, y)
    points = np.vstack([xv.ravel(), yv.ravel()]).T[:n]
    return points, dict(s=4, color=ORANGE)


def get_edges(graph: nx.Graph) -> list[tuple[int, int, dict]]:
    return [(e1, e2, dict(color=GREY)) for e1, e2 in graph.edges()]


if __name__ == '__main__':
    draw('grid.png', get_nodes, get_edges)
