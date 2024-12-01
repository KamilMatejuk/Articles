import networkx as nx
import pandas as pd

from simulator_threshold import SimluatorThresholdDeterministic, SimluatorThresholdStochastic


def load() -> nx.Graph:
    df = pd.read_csv('network_edges.csv')
    g = nx.Graph()
    for i, row in df.iterrows():
        g.add_edge(row['Person A'], row['Person B'])
        # if i == 1000: break
    print('INFO', len(g.nodes), 'nodes and', len(g.edges), 'edges')
    return g


if __name__ == '__main__':
    # g = load()
    g = nx.karate_club_graph()
    sim = SimluatorThresholdDeterministic(g, 10, 0, 'test', 0.3)
    sim.run()

