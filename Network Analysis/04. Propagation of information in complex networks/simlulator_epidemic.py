import enum
import random
import dataclasses
import networkx as nx

from simulator import Simluator, State


class TransitionType(enum.Enum):
    DURATION = enum.auto()
    PROBABILITY = enum.auto()
    PROBABILITY_FROM_NEIGHBORS = enum.auto()


@dataclasses.dataclass
class Transition:
    from_state: State
    to_state: State
    type: TransitionType
    value: float | int


class SimluatorEmpidemic(Simluator):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str):
        super().__init__(graph, max_iterations, starting_node, prefix)
        for n in self.graph.nodes:
            self.graph.nodes[n]['state_duration'] = 0
        self.transitions: list[Transition] = []
    
    def check(self, node):
        for transition in self.transitions:
            if transition.from_state != self.graph.nodes[node]['state']:
                # check only transitions from current state
                continue
            if transition.type == TransitionType.DURATION:
                # increment state duration
                self.graph.nodes[node]['state_duration'] += 1
                if self.graph.nodes[node]['state_duration'] >= transition.value:
                    self.graph.nodes[node]['state_duration'] = 0
                    return transition.to_state
            if transition.type == TransitionType.PROBABILITY:
                # check probability of auto-transition on its own
                if random.random() < transition.value:
                    return transition.to_state
            if transition.type == TransitionType.PROBABILITY_FROM_NEIGHBORS:
                # check probability of infection for each neighbor
                for n in self.graph.neighbors(node):
                    if self.graph.nodes[n]['state'] != State.INFECTED:
                        continue
                    if random.random() < transition.value:
                        return transition.to_state
        return self.graph.nodes[node]['state']


class SimluatorEmpidemicSI(SimluatorEmpidemic):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str,
                 susceptible_to_infected_probability: float):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.INFECTED, TransitionType.PROBABILITY_FROM_NEIGHBORS, susceptible_to_infected_probability),
        ]


class SimluatorEmpidemicSIR(SimluatorEmpidemic):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str,
                 susceptible_to_infected_probability: float, infected_to_recovered_duration: int):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.INFECTED, TransitionType.PROBABILITY_FROM_NEIGHBORS, susceptible_to_infected_probability),
            Transition(State.INFECTED, State.RECOVERED, TransitionType.DURATION, infected_to_recovered_duration),
        ]


class SimluatorEmpidemicSIS(SimluatorEmpidemic):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str,
                 susceptible_to_infected_probability: float, infected_to_susceptible_duration: int):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.INFECTED, TransitionType.PROBABILITY_FROM_NEIGHBORS, susceptible_to_infected_probability),
            Transition(State.INFECTED, State.SUSCEPTIBLE, TransitionType.DURATION, infected_to_susceptible_duration),
        ]


class SimluatorEmpidemicSEIR(SimluatorEmpidemic):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str,
                 SUSCEPTIBLE_to_exposed_probability: float,
                 exposed_to_infected_duration: int,
                 infected_to_recovered_duration: int):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.graph.nodes[self.starting_node]['state'] = State.EXPOSED
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.EXPOSED, TransitionType.PROBABILITY_FROM_NEIGHBORS, SUSCEPTIBLE_to_exposed_probability),
            Transition(State.EXPOSED, State.INFECTED, TransitionType.DURATION, exposed_to_infected_duration),
            Transition(State.INFECTED, State.RECOVERED, TransitionType.DURATION, infected_to_recovered_duration),
        ]


class SimluatorEmpidemicSEIS(SimluatorEmpidemic):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str,
                 SUSCEPTIBLE_to_exposed_probability: float,
                 exposed_to_infected_duration: int,
                 infected_to_susceptible_duration: int):
        super().__init__(graph, max_iterations, starting_node, prefix)
        self.graph.nodes[self.starting_node]['state'] = State.EXPOSED
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.EXPOSED, TransitionType.PROBABILITY_FROM_NEIGHBORS, SUSCEPTIBLE_to_exposed_probability),
            Transition(State.EXPOSED, State.INFECTED, TransitionType.DURATION, exposed_to_infected_duration),
            Transition(State.INFECTED, State.SUSCEPTIBLE, TransitionType.DURATION, infected_to_susceptible_duration),
        ]