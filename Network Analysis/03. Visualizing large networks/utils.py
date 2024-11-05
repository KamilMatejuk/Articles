import matplotlib.pyplot as plt
from typing import Callable
import networkx as nx
import pandas as pd
import numpy as np
import time
import tqdm
import sys
import os


GREY = '#999999'
ORANGE = '#fa3e08'


class Timer():
    def __init__(self, label: str, registry_ref: dict, steps: int = 1):
        self.label = label
        self.registry_ref = registry_ref
        self.steps = steps

    def __enter__(self):
        self.pbar = tqdm.tqdm(total=self.steps, desc=self.label)
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.elapsed = time.perf_counter() - self.start
        self.registry_ref[self.label] = self.elapsed
        self.pbar.desc = f'{self.label:<20s} {format_time_s(self.elapsed):>15s}'
        self.pbar.desc = f'{self.pbar.desc}'
        self.pbar.n = self.steps
        self.pbar.close()

    def step(self):
        self.pbar.update(1)

def format_time_s(time: int):
    formatted = ''
    for label, multiplier in [
        ('h', 60 * 60),
        ('m', 60),
        ('s', 1),
    ]:
        value = time // multiplier
        if value > 0:
            time -= value * multiplier
            formatted += f'{int(value)}{label} '
    formatted += f'{int(time * 1000)}ms'
    return formatted.strip()


def sort_by_degree(g: nx.Graph):
    return [n for n, _ in sorted(dict(g.degree()).items(), key=lambda x: x[1], reverse=True)]


def apply_alpha_based_on_degree(color: str, degree: int, min_degree: int = 1, max_degree: int = 256):
    alpha = int((degree - min_degree) / (max_degree - min_degree) * 256)
    if alpha > 200: return f'{color}{alpha:02x}'
    return f'{color}00'


def load() -> nx.Graph:
    df = pd.read_csv('network_edges.csv')
    g = nx.Graph()
    for i, row in df.iterrows():
        g.add_edge(row['Person A'], row['Person B'])
        # if i == 1000: break
    print('INFO', len(g.nodes), 'nodes and', len(g.edges), 'edges')
    return g


def draw(filename: str,
         get_nodes: Callable[[nx.Graph], tuple[np.ndarray, dict]],
         get_edges: Callable[[nx.Graph], list[tuple[int, int, dict]]]):

    graph = load()
    plt.figure(figsize=(12, 12))
    times = {}

    with Timer('Calculating nodes', times):
        nodes, node_kwargs = get_nodes(graph)

    with Timer('Drawing nodes', times):
        plt.scatter(nodes[:, 0], nodes[:, 1], zorder=2, **node_kwargs)

    with Timer('Calculating edges', times):
        edges = get_edges(graph)

    with Timer('Drawing edges', times, len(edges)) as timer:
        nodes_ids = list(graph.nodes)
        for e1, e2, kwargs in edges:
            coordinates = np.array([nodes[nodes_ids.index(e1)], nodes[nodes_ids.index(e2)]])
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, **kwargs)
            timer.step()

    with Timer('Saving', times):
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()
        plt.savefig(os.path.join('results', filename))
    
    return times


def benchmark(n: int, *draw_args, **draw_kwargs):
    times = []
    for i in range(n):
        print(f'\nBenchmark {i+1}/{n}\n')
        t = draw(*draw_args, **draw_kwargs)
        times.append(t)
    
    times = pd.DataFrame(times)
    print(f'\n{times}\n')
    
    print('Average in CSV format')
    means = pd.DataFrame(times.mean()).T.map(format_time_s)
    stds = pd.DataFrame(times.std()).T.map(format_time_s)
    all = means + '+-' + stds
    all.to_csv(sys.stdout, index=False)

