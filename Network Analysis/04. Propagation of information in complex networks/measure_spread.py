import tqdm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from simulator import State
from simlulator_epidemic import SimluatorEmpidemicSEIR


def get_spread(graph: nx.Graph, start_node: str) -> tuple[int, int]:
    sim = SimluatorEmpidemicSEIR(graph, 100, start_node, f'spread_{start_node}', 0.15, 1, 3)
    for _ in range(sim.max_iterations - 1):
        sim.run_iteration()
        sim.update_stats()
        if len(sim.stats[State.SUSCEPTIBLE][-1]) == 0: break
        if len(sim.stats[State.INFECTED][-1]) == 0: break
    infected = len(sim.stats[State.INFECTED][-1])
    recovered = len(sim.stats[State.RECOVERED][-1])
    return (infected + recovered) / len(graph.nodes), len(sim.stats[State.INFECTED])


def show_spreads(nodes: list[str], reached_ratios: list[float], iterations: list[int], filename: str):
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 5))
    axes[0].bar(range(len(nodes)), reached_ratios, color='#E4572E', width=0.85)
    axes[1].bar(range(len(nodes)), [-i for i in iterations], color='#3BBA6C', width=0.85)
    axes[1].set_xticks(range(len(nodes)), nodes, rotation=90)
    axes[0].tick_params(axis='y', colors='#E4572E')
    axes[1].tick_params(axis='y', colors='#3BBA6C')
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0%}'))
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{-int(x):d}'))
    axes[1].set_xlim(-0.55, len(nodes)-0.5)
    axes[0].set_ylabel('reached ratio')
    axes[1].set_ylabel('iterations')

    axes[0].set_ylim(0.3, 0.55)
    axes[1].set_ylim(-18, -14)
    tick_labels = axes[1].get_xticklabels()
    tick_labels[1].set_color('red')

    fig.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(filename)


def graph_spread_from_each_node():
    g = nx.les_miserables_graph()
    nodes, reached_ratios, iterations = [], [], []
    for n in tqdm.tqdm(g.nodes):
        nodes.append(n)
        irs = []
        its = []
        for _ in range(5):
            ir_i, it_i = get_spread(g, n)
            irs.append(ir_i)
            its.append(it_i)
        reached_ratios.append(np.mean(irs))
        iterations.append(np.mean(its))
    # sort all 3 by values from first list
    reached_ratios, iterations, nodes = map(list, zip(*sorted(zip(reached_ratios, iterations, nodes), reverse=True)))
    show_spreads(nodes, reached_ratios, iterations, 'images/reach_all_seir_ir_0.05_1_4.png')
    print('avg reached_ratios', np.mean(reached_ratios))
    print('avg iterations', np.mean(iterations))


def graph_spread_with_each_node_removed():
    g = nx.les_miserables_graph()
    nodes, reached_ratios, iterations = [], [], []
    for n in tqdm.tqdm([None] + list(g.nodes)):
        nodes.append(f'Removed {n}' if n else 'Original')

        g_i = g.copy()
        if n: g_i.remove_node(n)
        
        irs, its = [], []
        for n_i in tqdm.tqdm(g_i.nodes, leave=False):
            for _ in range(5):
                ir_i, it_i = get_spread(g_i, n_i)
                irs.append(ir_i)
                its.append(it_i)
        reached_ratios.append(np.mean(irs))
        iterations.append(np.mean(its))
        with open('log', 'a+') as f: f.write(f'{nodes[-1]}\t{reached_ratios[-1]:.2f}\t{iterations[-1]:.2f}\n')
    
    # sort all 3 by values from first list
    reached_ratios, iterations, nodes = map(list, zip(*sorted(zip(reached_ratios, iterations, nodes), reverse=True)))
    show_spreads(nodes, reached_ratios, iterations, 'images/reach_removed_seir_ir_0.15_1_3-new.png')
    print('avg reached_ratios', np.mean(reached_ratios))
    print('avg iterations', np.mean(iterations))


if __name__ == '__main__':
    # graph_spread_from_each_node()
    # graph_spread_with_each_node_removed()
    pass
