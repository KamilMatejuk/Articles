import networkx as nx
import pandas as pd

from simlulator_epidemic import SimluatorEmpidemicSI
from simlulator_epidemic import SimluatorEmpidemicSIR
from simlulator_epidemic import SimluatorEmpidemicSIS
from simlulator_epidemic import SimluatorEmpidemicSEIR
from simlulator_epidemic import SimluatorEmpidemicSEIS
from simlulator_cascade import SimluatorCascadeStochastic
from simulator_threshold import SimluatorThresholdStochastic
from simulator_threshold import SimluatorThresholdDeterministic


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
    sim = SimluatorEmpidemicSEIR(g, 10, 0, 'test', 0.3, 1, 2)
    sim.run()

