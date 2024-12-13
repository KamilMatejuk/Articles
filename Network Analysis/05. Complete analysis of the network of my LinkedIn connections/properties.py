import os
import tqdm
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import Callable, Any

from utils import load, get_node_rank


COLOR = '#FF3C00'
COLOR_RANK_1 = '#E4572E'
COLOR_RANK_2 = '#6290C3'
COLOR_RANK_3 = '#3BBA6C'


def plot_distribution(values: list[float | int], filename: str, log: bool = True):
    fig, ax = plt.subplots(figsize=(12, 4))
    bins = 50
    width = 0.9 * (max(values) - min(values)) / bins
    if isinstance(values[0], int) and width < 0.9: width = 0.9
    
    hist, bins = np.histogram(values, bins=bins, density=False)
    ax.bar(bins[:-1], hist, width=width, color=COLOR)
    ax.set_ylabel('Frequency')
    if log: ax.set_yscale('log')
    fig.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if log: filename = filename.replace('.png', '_log.png')
    plt.savefig(f'images/{filename}')


def get_distribution(
        graph: nx.Graph, func: Callable[[nx.Graph, str], float | int], description: str, preprocess_func: Callable[[nx.Graph], Any] = None
    ) -> tuple[list[float | int], list[float | int], list[float | int]]:

    filename = os.path.join('logs', description.replace(' ', '_').lower() + '.csv')
    if os.path.exists(filename): data = pd.read_csv(filename)
    else: data = pd.DataFrame(columns=['Node', 'Value'])
    
    preprocessed: Any = None
    n = len(graph.nodes())
    
    with tqdm.tqdm(graph.nodes(), desc=description) as pbar:
        for node in pbar:
            # don't repeat if already calculated
            if len(data) == n:
                pbar.total = len(data)
                pbar.n = len(data)
                continue
            if node in data['Node'].values:
                continue
            
            # preprocess
            if preprocess_func is not None:
                if preprocessed is None:
                    preprocessed = preprocess_func(graph)

            # calculate
            v = func(graph, node) if preprocessed is None else func(preprocessed, node)
            
            # save to in-memory object
            data = pd.concat([data, pd.DataFrame([{'Node': [node], 'Value': [v]}])], ignore_index=True)
            
            # save to file
            if len(data) == 1:
                data.to_csv(filename, index=False)
            else:
                with open(filename, 'a+') as f:
                    f.write(f'{node},{v}\n')

    data['rank'] = data['Node'].apply(lambda n: get_node_rank(graph, n))
    return (data[data['rank'] == 1]['Value'].tolist(),
            data[data['rank'] == 2]['Value'].tolist(),
            data[data['rank'] == 3]['Value'].tolist())


def plot_degree_distribution(graph: nx.Graph):
    values = get_distribution(graph, nx.degree, 'Degree distribution')
    print('me', values[0][0])
    print(f'my connections: avg {np.mean(values[1])} median {np.median(values[1])}')
    print(f'connections of my connections: avg {np.mean(values[2])} median {np.median(values[2])}')
    plot_distribution(values[1], 'dist_degree_2.png')
    plot_distribution(values[2], 'dist_degree_3.png')


def plot_betweenness_centrality_distribution(graph: nx.Graph):
    values = get_distribution(graph, lambda bc, n: bc[n], 'Betweenness centrality distribution', lambda g: nx.betweenness_centrality(g, k=1000))
    print('me', values[0][0])
    print(f'my connections: avg {np.mean(values[1])} median {np.median(values[1])}')
    print(f'connections of my connections: avg {np.mean(values[2])} median {np.median(values[2])}')
    plot_distribution(values[1], 'dist_betweenness_centrality_2.png')
    plot_distribution(values[2], 'dist_betweenness_centrality_3.png')


def plot_closeness_centrality_distribution(graph: nx.Graph):
    values = get_distribution(graph, nx.closeness_centrality, 'Closeness centrality distribution')
    print('me', values[0][0])
    print(f'my connections: avg {np.mean(values[1])} median {np.median(values[1])}')
    print(f'connections of my connections: avg {np.mean(values[2])} median {np.median(values[2])}')
    plot_distribution(values[1], 'dist_closeness_centrality_2.png')
    plot_distribution(values[2], 'dist_closeness_centrality_3.png')


def plot_shortest_path_distribution(graph: nx.Graph):
    def func(g: nx.Graph, node: str):
        path_lens = []
        for n in g.nodes():
            if n == node: continue
            path_lens.append(nx.shortest_path_length(g, node, n))
        return np.mean(path_lens)
    values = get_distribution(graph, func, 'Shortest path distribution')
    print('me', values[0][0])
    print(f'my connections: avg {np.mean(values[1])} median {np.median(values[1])}')
    print(f'connections of my connections: avg {np.mean(values[2])} median {np.median(values[2])}')
    plot_distribution(values[1], 'dist_shortest_path_2.png')
    plot_distribution(values[2], 'dist_shortest_path_3.png')


if __name__ == '__main__':
    g = load()
    print(f'Loaded graph with {len(g.nodes)} nodes and {len(g.edges)} edges')
    plot_degree_distribution(g)
    plot_betweenness_centrality_distribution(g)
    plot_closeness_centrality_distribution(g)
    plot_shortest_path_distribution(g)
