import networkx as nx

from simlulator_epidemic import SimluatorEmpidemicSI
from simlulator_epidemic import SimluatorEmpidemicSIR
from simlulator_epidemic import SimluatorEmpidemicSIS
from simlulator_epidemic import SimluatorEmpidemicSEIR
from simlulator_epidemic import SimluatorEmpidemicSEIS
from simlulator_cascade import SimluatorCascadeStochastic
from simulator_threshold import SimluatorThresholdStochastic
from simulator_threshold import SimluatorThresholdDeterministic


if __name__ == '__main__':
    g = nx.les_miserables_graph()
    
    closeness_centrality = nx.closeness_centrality(g)
    start_node = max(closeness_centrality, key=closeness_centrality.get)

    sim = SimluatorEmpidemicSEIR(g, 20, start_node, 'spread_all_epidemic_seir_0.25_1_2', 0.25, 1, 2)
    sim.run()

