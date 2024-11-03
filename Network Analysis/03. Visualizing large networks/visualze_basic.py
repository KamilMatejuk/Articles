import networkx as nx
import numpy as np

from utils import benchmark, draw, ORANGE, GREY


def get_nodes_random(graph: nx.Graph) -> tuple[np.ndarray, dict]:
    points = np.random.rand(len(graph.nodes), 2)
    return points, dict(s=4, color=ORANGE)


def get_nodes_grid(graph: nx.Graph) -> tuple[np.ndarray, dict]:
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


def get_nodes_circle(graph: nx.Graph) -> tuple[np.ndarray, dict]:
    n = len(graph.nodes())
    # calculate angles and distances in radial coordinates
    t = np.linspace(0, 2 * np.pi, n)
    # convert to cartesian coordinates
    x = np.cos(t)
    y = np.sin(t)
    points = np.vstack([x, y]).T
    return points, dict(s=4, color=ORANGE)


def get_nodes_spiral(graph: nx.Graph) -> tuple[np.ndarray, dict]:
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
    for get_nodes_function in [
        get_nodes_random,
        get_nodes_grid,
        get_nodes_circle,
        get_nodes_spiral,
    ]:
        print(f'\n{get_nodes_function}\n')
        img_label = get_nodes_function.__name__.replace('get_nodes_', '').strip()
        # draw(f'basic_{img_label}.png', get_nodes_function, get_edges)
        benchmark(5, f'basic_{img_label}.png', get_nodes_function, get_edges)
