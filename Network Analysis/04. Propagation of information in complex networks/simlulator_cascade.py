import random
import networkx as nx

from simulator import Simluator, State


class SimluatorCascadeStochastic(Simluator):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str, threshold: float):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.threshold = threshold
        self.infection_tries = set()

    def check(self, node):
        if self.graph.nodes[node]['state'] == State.INFECTED:
            return State.INFECTED
        for n in self.graph.neighbors(node):
            if self.graph.nodes[n]['state'] != State.INFECTED:
                # only infected can try to infect you
                continue
            if (n, node) in self.infection_tries:
                # already tried, cannot again
                return State.SUSEPTABLE
            # tries infecting
            self.infection_tries.add((n, node))
            r = random.random()
            if r >= self.threshold:
                return State.INFECTED
        return State.SUSEPTABLE
    
