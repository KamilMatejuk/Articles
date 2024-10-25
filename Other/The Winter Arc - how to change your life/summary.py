import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


COLOR_SUCCESSRATE_GREY = '#b0b0b0'
COLOR_SUCCESSRATE_MAIN = '#00cc00'


def time_to_float(time: str) -> float:
    if time == '0': return 0
    total = 0
    for part in time.split(' '):
        unit = part[-1]
        factor = {'h': 60, 'm': 1}[unit]
        val = part[:-1].replace(',', '.')
        total += float(val) * factor
    return total


def bars_with_threshold(ax1: plt.Axes, ax2: plt.Axes, threshold: str | int,
                        values: list[str | int], color: str,
                        values2: list[str | int] = None, color2: str = None,
                        is_time: bool = True, threshold_is_min: bool = True) -> None:
    if is_time:
        values = list(map(time_to_float, values))
        if values2: values2 = list(map(time_to_float, values2))
        threshold = time_to_float(threshold)
    total_values = [v1 + v2 for v1, v2 in zip(values, values2)] if values2 else values

    ax1.bar(range(len(values)), values, color=color)
    if values2: ax1.bar(range(len(values2)), values2, bottom=values, color=color2, label='nap')
    if values2: ax1.legend()
    ax1.axhline(threshold, color='red', linestyle='dotted')
    ax1.set_xticks(range(len(values)))
    ax1.set_xlim(-0.5, len(values) - 0.5)
    ax1.set_xticklabels(range(1, 1 + len(values)))
    if is_time:
        if (max(total_values) // 60) > 1:
            ticks = range(1, int(max(total_values) // 60) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax1.set_yticks([60 * i for i in ticks])
            ax1.set_yticklabels([f'{i}h' for i in ticks])
        else:
            ticks = range(1, int(max(total_values) // 5) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax1.set_yticks([5 * i for i in ticks])
            ax1.set_yticklabels([f'{5*i}m' for i in ticks])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    if threshold_is_min:
        success = sum(v >= threshold for v in total_values)
    else:
        success = sum(v <= threshold for v in total_values)
    wedges, _ = ax2.pie([success, len(total_values) - success], startangle=90,
                        colors=[COLOR_SUCCESSRATE_MAIN, COLOR_SUCCESSRATE_GREY])
    wedges[0].set(width=0.3)
    wedges[1].set(width=0.3, linewidth=8, edgecolor='white')
    ax2.text(0, 0, f'{success/len(total_values):.0%}', ha='center', va='center', fontsize=16)
    ax2.text(0, -1.3, f'success rate', ha='center', va='center', fontsize=12)


if __name__ == '__main__':
    rows = 6
    colors = [plt.cm.winter(i) for i in np.linspace(0, 1, rows + 1)]

    fig = plt.figure(figsize=(10, 2 * rows))
    gs = gridspec.GridSpec(rows, 2, width_ratios=[4, 1])

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax1.set_title('Side projects (minimum 15m daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, '15m', ['15m', '1h', '1h', '30m', '2h', '2h', '3h', '0', '0',
        '2h', '30m', '5h', '2,5h', '0', '0', '15m', '3h', '0', '0', '0', '0', '0', '1h', '1h'],
        colors[0])

    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax1.set_title('Reading (minimum 5m daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, '5m', ['15m', '15m', '15m', '15m', '15m', '15m', '15m', '15m',
        '15m', '15m', '15m', '15m', '15m', '15m', '5m', '0', '15m', '15m', '0', '0', '15m', '15m',
        '15m', '0'], colors[1])

    ax1 = fig.add_subplot(gs[2, 0])
    ax2 = fig.add_subplot(gs[2, 1])
    ax1.set_title('Exercise (minimum 10m daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, '10m', ['2.5h', '20m', '1.5h', '1h', '0', '3h', '0', '3h', '5m',
        '0', '2.5h', '20m', '0', '1h', '1.5h', '1h', '0', '2h', '4h', '0', '0', '2.5h', '10m',
        '1.5h'], colors[2])

    ax1 = fig.add_subplot(gs[3, 0])
    ax2 = fig.add_subplot(gs[3, 1])
    ax1.set_title('Sleep (minimum 7h daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, '7h', ['7h', '6h', '7,5h', '5h', '6h', '10h', '6.5h', '5,5h',
        '6,5h', '7,5h', '5,5h', '9h', '7,5h', '6h', '6,5h', '9h', '7h', '7h', '7,5h', '11h', '5h',
        '5,5h', '7h', '7h'], colors[3], ['0', '0', '0', '3h', '0', '0', '2h', '0', '0', '3h',
        '1,5h', '3h', '0', '0', '0', '0', '0', '2h', '0', '2h', '3h', '0', '0', '1h'], colors[4])

    ax1 = fig.add_subplot(gs[4, 0])
    ax2 = fig.add_subplot(gs[4, 1])
    ax1.set_title('Calories (minimum 2900 kcal daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, 2900, [1826, 3179, 2783, 2145, 2361, 2222, 2325, 1796, 2860, 2789,
        2537, 3148, 2458, 2756, 2224, 2898, 2629, 2131, 0, 1487, 2349, 2822, 3640, 2465], colors[5],
        is_time=False)

    ax1 = fig.add_subplot(gs[5, 0])
    ax2 = fig.add_subplot(gs[5, 1])
    ax1.set_title('Phone usage (maximum 4h daily)', fontsize=14)
    bars_with_threshold(ax1, ax2, '4h', ['3h 32m', '5h 19m', '3h 11m', '4h 30m', '1h 4m', '2h 29m',
        '3h 17m', '4h 55m', '6h 8m', '4h 26m', '3h 57m', '54m', '2h 36m', '4h 11m', '3h 25m',
        '3h 17m', '3h 48m', '3h 25m', '1h 13m', '1h 4m', '4h 26m', '3h 57m', '3h 31m', '2h 19m'],
        colors[6], threshold_is_min=False)

    plt.tight_layout()
    fig.subplots_adjust(hspace=0.75)
    plt.savefig('summary.png')
