import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from simulator import State
from simlulator_epidemic import SimluatorEmpidemicSEIR


def get_spread(graph: nx.Graph, start_node: str) -> tuple[int, int]:
    sim = SimluatorEmpidemicSEIR(graph, 20, start_node, f'spread_{start_node}', 0.15, 1, 3)
    for _ in range(sim.max_iterations - 1):
        sim.run_iteration()
        sim.update_stats()
        if len(sim.stats[State.SUSCEPTIBLE][-1]) == 0: break
        if len(sim.stats[State.INFECTED][-1]) == 0: break
    return len(sim.stats[State.INFECTED][-1]) / len(graph.nodes), len(sim.stats[State.INFECTED])


def show_spreads(nodes: list[str], infected_ratios: list[float], iterations: list[int], filename: str):
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 5))
    axes[0].bar(range(len(nodes)), infected_ratios, color='#E4572E', width=0.85)
    axes[1].bar(range(len(nodes)), [-i for i in iterations], color='#3BBA6C', width=0.85)
    axes[1].set_xticks(range(len(nodes)), nodes, rotation=90)
    axes[0].tick_params(axis='y', colors='#E4572E')
    axes[1].tick_params(axis='y', colors='#3BBA6C')
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0%}'))
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{-int(x):d}'))
    axes[1].set_xlim(-0.55, len(nodes)-0.5)
    axes[0].set_ylabel('infected ratio')
    axes[1].set_ylabel('iterations')
    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(filename)


if __name__ == '__main__':
    g = nx.les_miserables_graph()
    nodes, infected_ratios, iterations = [], [], []
    for i, n in enumerate(g.nodes):
        nodes.append(n)
        irs = []
        its = []
        for _ in range(5):
            ir_i, it_i = get_spread(g, n)
            irs.append(ir_i)
            its.append(it_i)
        infected_ratios.append(np.mean(irs))
        iterations.append(np.mean(its))
        print(i)
    
    # sort all 3 by values from first list
    infected_ratios, iterations, nodes = map(list, zip(*sorted(zip(infected_ratios, iterations, nodes), reverse=True)))

    show_spreads(nodes, infected_ratios, iterations, 'images/reach_all_seir_0.15_1_3.png')
    
    print(np.mean(infected_ratios))
    print(np.mean(iterations))
