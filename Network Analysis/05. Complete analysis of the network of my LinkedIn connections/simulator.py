import matplotlib.pyplot as plt
from enum import Enum, auto
from io import BytesIO
import networkx as nx
import numpy as np
import dataclasses
import random
import imageio
import tqdm
import os


from utils import load, get_node_rank, get_circular_positions


class State(Enum):
    SUSCEPTIBLE = '#3BBA6C'
    EXPOSED = '#ECF452'
    INFECTED = '#E4572E'
    RECOVERED = '#6290C3'


class TransitionType(Enum):
    DURATION = auto()
    PROBABILITY = auto()
    PROBABILITY_FROM_NEIGHBORS = auto()


@dataclasses.dataclass
class Transition:
    from_state: State
    to_state: State
    type: TransitionType
    value: float | int


class SimluatorEmpidemicSEIR:
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str, susceptible_to_exposed_probability: float,
                 exposed_to_infected_duration: int, infected_to_recovered_duration: int):
        self.graph = graph
        graph_points_dict = nx.kamada_kawai_layout(graph)
        self.graph_pos = np.array([graph_points_dict[n] for n in graph.nodes])
        # params
        self.iteration = 1
        self.max_iterations = max_iterations
        self.prefix = prefix
        # first infection
        self.starting_node = starting_node
        self.stats: dict[State, list[list]] = {s: [] for s in State}
        for n in self.graph.nodes:
            self.graph.nodes[n]['state_duration'] = 0
            if n == self.starting_node:
                self.graph.nodes[n]['state'] = State.EXPOSED
            else:
                self.graph.nodes[n]['state'] = State.SUSCEPTIBLE
        self.update_stats()
        # transitions
        self.transitions = [
            Transition(State.SUSCEPTIBLE, State.EXPOSED, TransitionType.PROBABILITY_FROM_NEIGHBORS, susceptible_to_exposed_probability),
            Transition(State.EXPOSED, State.INFECTED, TransitionType.DURATION, exposed_to_infected_duration),
            Transition(State.INFECTED, State.RECOVERED, TransitionType.DURATION, infected_to_recovered_duration),
        ]
    
    def update_stats(self):
        for s in State:
            self.stats[s].append([n for n, v in self.graph.nodes.items() if v['state'] == s])
    
    def log(self):
        print(f'iter {str(self.iteration):<3s} | ' + ' | '.join(f'{s.name[0]} {str(len(self.stats[s][-1])):>3s}' for s in State))

    def run_iteration(self):
        new_states: dict[str, State] = {}
        for node in self.graph.nodes:
            new_states[node] = self.check(node)
        for node, state in new_states.items():
            self.graph.nodes[node]['state'] = state
        self.iteration += 1
    
    def run(self):
        self.log()
        for _ in range(self.max_iterations - 1):
            self.run_iteration()
            self.update_stats()
            self.log()
            if len(self.stats[State.SUSCEPTIBLE][-1]) == 0: break
            if len(self.stats[State.INFECTED][-1]) == 0: break
        self.generate_gif()
    
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

    def generate_gif(self):
        images = []
        for i in range(self.iteration):
            images.append(self.generate_gif_frame(i + 1))
        total_duration = 20
        images.extend(image.copy() for image in reversed(images[1:-1])) # reverse
        imageio.mimsave(os.path.join('images', f'{self.prefix}.gif'), images, loop=0, duration=1000 * total_duration / len(images))
    
    def generate_gif_frame(self, iteration: int):
        fig = plt.figure(figsize=(12, 6.5))
        gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
        ax1 = fig.add_subplot(gs[0])
        self.generate_gif_graph(ax1, iteration)
        ax2 = fig.add_subplot(gs[1])
        self.generate_gif_stats(ax2, iteration)
        fig.suptitle(f'Iteration {iteration}', fontsize=16)
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return imageio.v2.imread(buf)

    def generate_gif_graph(self, ax: plt.Axes, iteration: int):
        for s in self.stats:
            for n in self.stats[s][iteration-1]:
                self.graph.nodes[n]['state'] = s
        positions = {'me': (0, 0)}
        nodes_2 = [n for n in self.graph.nodes if n != 'me']
        # me
        x, y = positions['me']
        ax.scatter(x, y, zorder=2, s=50, c=self.graph.nodes['me']['state'].value)
        # my connections
        pos = get_circular_positions(1, len(self.graph.nodes)-1)
        colors = [self.graph.nodes[n]['state'].value for n in nodes_2]
        plt.scatter(pos[:, 0], pos[:, 1], zorder=2, s=50, c=colors)
        for node, (x, y) in zip(nodes_2, pos):
            positions[node] = (x, y)
        for e1, e2 in tqdm.tqdm(self.graph.edges):
            if e1 not in positions or e2 not in positions: continue
            coordinates = np.array([positions[e1], positions[e2]])
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color=f'#99999955', linewidth=0.5)
        ax.axis('off')

    def generate_gif_stats(self, ax: plt.Axes, iteration: int):
        non_zero_states = [s for s in State if any(ss != 0 for ss in self.stats[s])]
        ax.stackplot(range(iteration), [list(map(len, self.stats[s][:iteration])) for s in non_zero_states],
                      labels=[s.name for s in non_zero_states],
                      colors=[s.value for s in non_zero_states])
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Number of nodes')
        ax.set_xlim(0, self.iteration - 1)
        ax.set_ylim(0, len(self.graph.nodes))
        ax.set_xticks(range(0, self.iteration), range(1, self.iteration + 1))
        ax.legend()


if __name__ == '__main__':
    g = load()
    nodes_3 = [n for n in g.nodes if get_node_rank(g, n) == 3]
    g.remove_nodes_from(nodes_3)    
    sim = SimluatorEmpidemicSEIR(g, 20, 'me', 'spread_all_epidemic_seir_0.15_1_3', 0.15, 1, 3)
    sim.run()
