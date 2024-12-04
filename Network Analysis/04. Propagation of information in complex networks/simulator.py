from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
from enum import Enum
from pathlib import Path
from io import BytesIO
import networkx as nx
from glob import glob
import numpy as np
import imageio
import os

from visualisator import Visualisator


class State(Enum):
    SUSEPTABLE = '#3BBA6C'
    EXPOSED = '#ECF452'
    INFECTED = '#E4572E'
    RECOVERED = '#6290C3'


class Simluator(ABC):
    def __init__(self, graph: nx.Graph, max_iterations: int, starting_node: str, prefix: str):
        self.graph = graph
        graph_points_dict = nx.kamada_kawai_layout(graph)
        self.graph_pos = np.array([graph_points_dict[n] for n in graph.nodes])
        # params
        self.iteration = 1
        self.max_iterations = max_iterations
        self.prefix = prefix
        os.makedirs('results', exist_ok=True)
        # first infection
        self.starting_node = starting_node
        self.stats: dict[State, list[list]] = {s: [] for s in State}
        for n in self.graph.nodes:
            if n == self.starting_node:
                self.graph.nodes[n]['state'] = State.INFECTED
            else:
                self.graph.nodes[n]['state'] = State.SUSEPTABLE
        self.update_stats()
    
    def update_stats(self):
        for s in State:
            self.stats[s].append([n for n, v in self.graph.nodes.items() if v['state'] == s])
    
    def log(self):
        print(f'iter {str(self.iteration):<3s} | ' + ' | '.join(f'{s.name[0]} {str(len(self.stats[s][-1])):>3s}' for s in State))
        with open(os.path.join('results', f'{self.prefix}.log'), 'a+') as f:
            f.write(','.join([str(self.iteration)] + [str(len(self.stats[s][-1])) for s in (
            State.SUSEPTABLE, State.EXPOSED, State.INFECTED, State.RECOVERED)]) + '\n')

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
            if len(self.stats[State.SUSEPTABLE][-1]) == 0: break
            if len(self.stats[State.INFECTED][-1]) == 0: break
        self.generate_gif()
    
    @abstractmethod
    def check(self, node) -> State:
        raise NotImplementedError

    def generate_gif(self):
        images = []
        for i in range(self.iteration):
            images.append(self.generate_gif_frame(i + 1))
        Visualisator.generate_gif(images, os.path.join('results', f'{self.prefix}.gif'), duration_ms=1000, reverse=True, interpolate_frames=10)
    
    def generate_gif_frame(self, iteration: int):
        fig = plt.figure(figsize=(12, 5))
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
        return imageio.imread(buf)

    def generate_gif_graph(self, ax: Axis, iteration: int):
        for s in self.stats:
            for n in self.stats[s][iteration-1]:
                self.graph.nodes[n]['state'] = s
        Visualisator.generate_graph(ax, self.graph, self.graph_pos)

    def generate_gif_stats(self, ax: Axis, iteration: int):
        non_zero_states = [s for s in State if any(ss != 0 for ss in self.stats[s])]
        ax.stackplot(range(iteration), [list(map(len, self.stats[s][:iteration])) for s in non_zero_states],
                      labels=[s.name for s in non_zero_states],
                      colors=[s.value for s in non_zero_states])
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Number of nodes')
        ax.set_xlim(0, self.iteration - 1)
        ax.set_ylim(0, len(self.graph.nodes))
        ax.set_xticks(range(0, self.iteration), range(1, self.iteration + 1))
