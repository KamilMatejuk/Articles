import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import tqdm


COLOR_NODE = '#fa3e08'
COLOR_EDGE = '#999999'


def sort_by_degree(g: nx.Graph):
    return [n for n, _ in sorted(dict(g.degree()).items(), key=lambda x: x[1], reverse=True)]


def apply_alpha_based_on_degree(color: str, degree: int, min_degree: int = 1, max_degree: int = 256):
    alpha = int((degree - min_degree) / (max_degree - min_degree) * 256)
    if alpha > 200: return f'{color}{alpha:02x}'
    return f'{color}00'


def draw(filename):
    def decorator(func):
        def wrapper(g: nx.Graph, figsize: tuple[int, int]):
            plt.figure(figsize=figsize)
            print('Calculating positions')
            nodes = sort_by_degree(g)
            min_degree, max_degree = g.degree(nodes[0]), g.degree(nodes[-1])
            node_points = func(g, figsize)
            print('Drawing nodes')
            plt.scatter(node_points[:, 0], node_points[:, 1], s=4, c=COLOR_NODE, zorder=2)
            for edge_nodes in tqdm.tqdm(g.edges(), desc='Drawing edges'):
                coordinates = np.array([node_points[nodes.index(n)] for n in edge_nodes])
                degrees = [g.degree(n) for n in edge_nodes]
                color = apply_alpha_based_on_degree(COLOR_EDGE, sum(degrees) / len(degrees), min_degree, max_degree)
                plt.plot(coordinates[:, 0], coordinates[:, 1], color=color, zorder=1)
            print(f'Saving to {filename}')
            plt.xlim(0, figsize[0])
            plt.ylim(0, figsize[1])
            plt.axis('off')
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.savefig(filename)
        return wrapper
    return decorator


@draw('network_grid.png')
def custom_draw_grid(g: nx.Graph, figsize: tuple[int, int]):
    width, height = figsize
    n = len(g.nodes())
    cols = int(np.ceil(np.sqrt(n * (width / height))))
    rows = int(np.ceil(n / cols))
    linspace = lambda size, items: np.linspace(0+size/items/3, size-size/items/3, items)
    x = linspace(width, cols)
    y = linspace(height, rows)
    xv, yv = np.meshgrid(x, y)
    points = np.vstack([xv.ravel(), yv.ravel()]).T[:n]
    return points


@draw('network_spiral.png')
def custom_draw_spiral(g: nx.Graph, figsize: tuple[int, int]):
    width, height = figsize
    n = len(g.nodes())
    turns = 15
    t = np.linspace(0, turns * 2 * np.pi, n)
    r = np.linspace(0, 1, n)
    x = r * np.cos(t)
    y = r * np.sin(t)
    scale = lambda data, size: (data - data.min()) / (data.max() - data.min()) * size * 0.95 + size * 0.025
    x_scaled = scale(x, width)
    y_scaled = scale(y, height)
    points = np.vstack([x_scaled, y_scaled]).T
    return points


@draw('network_circle.png')
def custom_draw_circle(g: nx.Graph, figsize: tuple[int, int]):
    width, height = figsize
    n = len(g.nodes())
    t = np.linspace(0, 2 * np.pi, n)
    x = np.cos(t)
    y = np.sin(t)
    scale = lambda data, size: (data - data.min()) / (data.max() - data.min()) * size * 0.95 + size * 0.025
    x_scaled = scale(x, width)
    y_scaled = scale(y, height)
    points = np.vstack([x_scaled, y_scaled]).T
    return points


if __name__ == '__main__':
    df = pd.read_csv('network_edges.csv')
    G = nx.Graph()
    for i, row in df.iterrows():
        G.add_edge(row['Person A'], row['Person B'])
        # if i == 10000: break
    print('Nodes', len(G.nodes))
    print('Edges', len(G.edges))
    custom_draw_grid(G, (12, 10))
    custom_draw_spiral(G, (12, 10))
    custom_draw_circle(G, (12, 10))
