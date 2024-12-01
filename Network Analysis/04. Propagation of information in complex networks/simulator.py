from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from enum import Enum
from pathlib import Path
import networkx as nx
from glob import glob
import numpy as np
import imageio
import os


GREY = '#999999'


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
        Path('results', prefix).mkdir(parents=True, exist_ok=True)
        # first infection
        self.starting_node = starting_node
        self.stats: dict[State, list[int]] = {s: [] for s in State}
        for n in self.graph.nodes:
            if n == self.starting_node:
                self.graph.nodes[n]['state'] = State.INFECTED
            else:
                self.graph.nodes[n]['state'] = State.SUSEPTABLE
        self.update_stats()
        self.save_img_iteration()
    
    def update_stats(self):
        for s in State:
            self.stats[s].append(len([n for n, v in self.graph.nodes.items() if v['state'] == s]))
    
    def run_iteration(self):
        new_states: dict[str, State] = {}
        for node in self.graph.nodes:
            new_states[node] = self.check(node)
        for node, state in new_states.items():
            self.graph.nodes[node]['state'] = state
        self.iteration += 1
    
    def run(self):
        for _ in range(self.max_iterations - 1):
            self.run_iteration()
            self.update_stats()
            self.save_img_iteration()
            if self.stats[State.SUSEPTABLE][-1] == 0: break
            if self.stats[State.INFECTED][-1] == 0: break
        self.save_img_stats()
        self.save_gif_iterations()
    
    @abstractmethod
    def check(self, node) -> State:
        raise NotImplementedError
    
    def save_img_iteration(self):
        plt.figure(figsize=(12, 12))
        nodes_ids = list(self.graph.nodes)
        colors = [n['state'].value for n in self.graph.nodes.values()]
        plt.scatter(self.graph_pos[:, 0], self.graph_pos[:, 1], zorder=2, c=colors, s=1000)
        for e1, e2 in self.graph.edges:
            coordinates = np.array([self.graph_pos[nodes_ids.index(e1)], self.graph_pos[nodes_ids.index(e2)]])
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color=GREY, linewidth=2)
        plt.axis('off')
        plt.xticks([])
        plt.yticks([])
        plt.suptitle(f'Iteration {self.iteration}', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join('results', self.prefix, f'iter_{self.iteration:04}.png'))

    def save_gif_iterations(self):
        files = sorted(list(glob(os.path.join('results', self.prefix, 'iter_*.png'))))
        images = []
        for filename in files:
            images.append(imageio.imread(filename))
        imageio.mimsave(os.path.join('results', self.prefix, 'iter.gif'), images, loop=0, duration=500)
        
    def save_img_stats(self):
        plt.figure(figsize=(9, 3))
        non_zero_states = [s for s in State if any(ss != 0 for ss in self.stats[s])]
        plt.stackplot(range(len(self.stats[State.SUSEPTABLE])), [self.stats[s] for s in non_zero_states],
                      labels=[s.name for s in non_zero_states],
                      colors=[s.value for s in non_zero_states])
        plt.xlabel('Iteration')
        plt.ylabel('Number of nodes')
        plt.xlim(0, len(self.stats[State.SUSEPTABLE]) - 1)
        plt.ylim(0, len(self.graph.nodes))
        plt.xticks(range(0, len(self.stats[State.SUSEPTABLE])), range(1, len(self.stats[State.SUSEPTABLE]) + 1))
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join('results', self.prefix, 'stats.png'))
