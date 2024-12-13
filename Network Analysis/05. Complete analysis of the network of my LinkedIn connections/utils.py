import networkx as nx
import pandas as pd


def load() -> nx.Graph:
    df = pd.read_csv('network_edges.csv')
    g = nx.Graph()
    for i, row in df.iterrows():
        g.add_edge(row['Person A'], row['Person B'])
        # if i == 1000: break
    print('INFO', len(g.nodes), 'nodes and', len(g.edges), 'edges')
    return g


def get_node_rank(graph: nx.Graph, node: str):
    if node == "me":
        return 1
    if node in graph.neighbors("me"):
        return 2
    return 3