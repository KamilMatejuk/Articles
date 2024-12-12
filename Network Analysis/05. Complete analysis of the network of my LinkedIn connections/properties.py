import os
import tqdm
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import Callable


COLOR = '#FF3C00'


def load() -> nx.Graph:
    df = pd.read_csv('network_edges.csv')
    g = nx.Graph()
    for i, row in df.iterrows():
        g.add_edge(row['Person A'], row['Person B'])
        # if i == 1000: break
    print('INFO', len(g.nodes), 'nodes and', len(g.edges), 'edges')
    return g


def plot_distribution(values: list[float | int], filename: str):
    fig, ax = plt.subplots(figsize=(12, 4))
    if isinstance(values[0], int):
        bins = range(min(values), max(values) + 2)
        width = 0.9
    else:
        bins = 25
        width = 0.9 * (max(values) - min(values)) / bins

    hist, bins = np.histogram(values, bins=bins, density=False)
    ax.bar(bins[:-1], hist, width=width, color=COLOR)
    ax.set_ylabel('Frequency')
    ax.set_yscale('log')
    fig.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig(f'images/{filename}')


def get_distribution(graph: nx.Graph, func: Callable[[nx.Graph, str], float | int], description: str):
    filename = description.replace(' ', '_').lower() + '.csv'
    if os.path.exists(filename): data = pd.read_csv(filename)
    else: data = pd.DataFrame(columns=['Node', 'Value'])
    
    with tqdm.tqdm(graph.nodes(), desc=description) as pbar:
        for node in pbar:
            # don't repeat if already calculated
            if len(data) == len(graph.nodes()):
                pbar.total = len(data)
                pbar.n = len(data)
                continue
            if node in data['Node'].values:
                continue
            
            # calculate
            v = func(graph, node)
            
            # save to in-memory object
            data = pd.concat([data, pd.DataFrame({'Node': [node], 'Value': [v]})], ignore_index=True)
            
            # save to file
            if len(data) == 1:
                data.to_csv(filename, index=False)
            else:
                with open(filename, 'a+') as f:
                    f.write(f'{node},{v}\n')

    return data['Value'].tolist()


def plot_degree_distribution(graph: nx.Graph, filename: str):
    values = get_distribution(graph, nx.degree, 'Degree distribution')
    plot_distribution(values, filename)


def plot_betweenness_centrality_distribution(graph: nx.Graph, filename: str):
    bc = nx.betweenness_centrality(graph)
    with open('bc.txt', 'w+') as f: f.write(str(bc))
    values = get_distribution(graph, lambda _, n: bc[n], 'Betweenness centrality distribution')
    plot_distribution(values, filename)


def plot_closeness_centrality_distribution(graph: nx.Graph, filename: str):
    cc = nx.closeness_centrality(graph)
    with open('cc.txt', 'w+') as f: f.write(str(cc))
    values = get_distribution(graph, lambda _, n: cc[n], 'Closeness centrality distribution')
    plot_distribution(values, filename)


def plot_shortest_path_distribution(graph: nx.Graph, filename: str):
    def func(g: nx.Graph, node: str):
        path_lens = []
        for n in g.nodes():
            if n == node: continue
            path_lens.append(nx.shortest_path_length(g, node, n))
        return np.mean(path_lens)
    values = get_distribution(graph, func, 'Shortest path distribution')
    plot_distribution(values, filename)


if __name__ == '__main__':
    g = load()
    print(f'Loaded graph with {len(g.nodes)} nodes and {len(g.edges)} edges')
    plot_degree_distribution(g, 'dist_degree.png')
    plot_betweenness_centrality_distribution(g, 'dist_betweenness_centrality.png')
    plot_closeness_centrality_distribution(g, 'dist_closeness_centrality.png')
    plot_shortest_path_distribution(g, 'dist_shortest_path.png')
