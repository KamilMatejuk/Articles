import re
import pandas as pd
import matplotlib.pyplot as plt


def time_to_float(time: str) -> float:
    total = 0
    for part in time.split(' '):
        unit = re.search(r'[a-z]+', part).group(0)
        value = int(part.replace(unit, ''))
        multiplier = { 'h': 60 * 60, 'm': 60, 's': 1, 'ms': 0.001 }.get(unit)
        total += value * multiplier
    return total


if __name__ == '__main__':
    fig, ax = plt.subplots(1, 1, figsize=(12, 3))
    
    data = pd.read_csv('compare_nx_basic.csv')
    for c in list(data.columns)[1:]:
        data[c] = data[c].apply(lambda x: time_to_float(x.split('±')[0]))
    
    for stage in range(len(data.columns) - 1):
        vals = data[list(data.columns)[stage + 1]]
        left = None if stage == 0 else data[list(data.columns)[1:stage + 1]].sum(axis=1)
        label = list(data.columns)[stage + 1]
        ax.barh(data["label"], vals, left=left, label=label)

    ax.set_xlabel("Time (seconds)", fontsize=14)
    ax.legend(loc="lower center", ncol=len(data.columns) - 1)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    
    fig.tight_layout()
    plt.savefig('compare_nx_basic.png')
