import random
import networkx as nx
from abc import abstractmethod

from simulator import Simluator, State


class SimluatorThreshold(Simluator):
    def get_number_of_neighbors(self, node):
        return len(list(self.graph.neighbors(node)))
    
    def get_number_of_infected_neighbors(self, node):
        return len([n for n in self.graph.neighbors(node) if self.graph.nodes[n]['state'] == State.INFECTED])
    
    def check(self, node):
        if self.graph.nodes[node]['state'] == State.INFECTED:
            return State.INFECTED
        if self.check_if_becomes_infected(node):
            return State.INFECTED
        return State.SUSEPTABLE
    
    @abstractmethod
    def check_if_becomes_infected(self, node):
        raise NotImplementedError


class SimluatorThresholdDeterministic(SimluatorThreshold):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str, threshold: float):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.threshold = threshold
    
    def check_if_becomes_infected(self, node):
        ratio = self.get_number_of_infected_neighbors(node) / self.get_number_of_neighbors(node)
        return ratio > self.threshold


class SimluatorThresholdStochastic(SimluatorThreshold):
    def check_if_becomes_infected(self, node):
        ratio = self.get_number_of_infected_neighbors(node) / self.get_number_of_neighbors(node)
        return random.random() < ratio
