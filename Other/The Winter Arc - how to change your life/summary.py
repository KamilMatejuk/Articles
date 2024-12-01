import numpy as np
import matplotlib.pyplot as plt


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


def float_to_time(time: float) -> str:
    h = int(time / 60)
    m = int(time - h * 60)
    return ((f'{h}h' if h else '') + ' ' + (f'{m}m' if m else '')).strip()


def bars_with_threshold(ax: plt.Axes, label: str, threshold: str | int,
                        values: list[str | int], color: str,
                        values2: list[str | int] = None, color2: str = None,
                        is_time: bool = True, threshold_is_min: bool = True,
                        omit_zeros_in_avg: bool = False) -> None:
    if is_time:
        values = list(map(time_to_float, values))
        if values2: values2 = list(map(time_to_float, values2))
        threshold = time_to_float(threshold)
    total_values = [v1 + v2 for v1, v2 in zip(values, values2)] if values2 else values

    ax.bar(range(len(values)), values, color=color)
    if values2: ax.bar(range(len(values2)), values2, bottom=values, color=color2, label='nap')
    if values2: ax.legend()
    ax.set_xticks(range(len(values)))
    ax.set_xlim(-0.5, len(values) - 0.5)
    ax.set_xticklabels(range(1, 1 + len(values)))
    ax.set_title(label)
    if is_time:
        if (max(total_values) // 60) > 1:
            ticks = range(1, int(max(total_values) // 60) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax.set_yticks([60 * i for i in ticks])
            ax.set_yticklabels([f'{i}h' for i in ticks])
        else:
            ticks = range(1, int(max(total_values) // 5) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax.set_yticks([5 * i for i in ticks])
            ax.set_yticklabels([f'{5*i}m' for i in ticks])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # threshold and 
    if omit_zeros_in_avg:
        non_zero_total_values = [v for v in total_values if v != 0]
        avg = int(sum(non_zero_total_values) / len(non_zero_total_values))
    else:
        avg = int(sum(total_values) / len(total_values))
    label_thd = ('minimum ' if threshold_is_min else 'maximum ') + (float_to_time(threshold) if is_time else f'{threshold:.0f}') + ' daily'
    label_avg = f'average ' + (float_to_time(avg) if is_time else f'{avg:.0f}') + ' daily'
    ax.axhline(threshold, color='#023020', linestyle='dotted')
    ax.axhline(avg, color='purple', linestyle='dotted')
    # fix overlapping texts
    dist = abs(threshold - avg) / max(total_values)
    if dist < 0.15:
        padd = (0.15 * max(total_values) - abs(threshold - avg)) / 2
        if threshold > avg: threshold_padded, avg_padded = threshold + padd, avg - padd
        else: threshold_padded, avg_padded = threshold - padd, avg + padd
    else: threshold_padded, avg_padded = threshold, avg
    ax.text(x=len(total_values), y=threshold_padded, s=label_thd, ha='left', va='center', fontsize=12, color='#023020')
    ax.text(x=len(total_values), y=avg_padded, s=label_avg, ha='left', va='center', fontsize=12, color='purple')

    if threshold_is_min:
        success = sum(v >= threshold for v in total_values)
    else:
        success = sum(v <= threshold for v in total_values)
    return success/len(total_values)


if __name__ == '__main__':
    rows = 6
    colors = [plt.cm.winter(i) for i in np.linspace(0, 1, rows + 1)]
    
    labels = ['Side projects', 'Reading', 'Exercise', 'Sleep', 'Calories', 'Phone usage',
              'Articles', 'Gym', 'Shoulder raises', 'Alcohol']

    fig, axes = plt.subplots(rows, 1, figsize=(12, 2 * rows))

    passrate_projects = bars_with_threshold(axes[0], labels[0], '15m',
        ['30m', '3h', '2h', '30m', '1h 45m', '2,5h', '4h', '3h', '4h', '0', '2h', '1.5h', '0', '0',
        '1,5h', '0', '0', '0', '0.5h', '15m', '2h', '2.5h', '0', '0', '0,5h', '2h', '15m', '4,5h',
        '15m', '0'], colors[0])

    passrate_reading = bars_with_threshold(axes[1], labels[1], '5m',
        ['25m', '50m', '0', '30m', '35m', '0', '0', '10m', '0', '0', '10m', '25m', '10m', '0', '0',
        '0', '10m', '0', '10m', '10m', '20m', '5m', '15m', '5m', '20m', '10m', '20m', '10m', '10m',
        '5m'], colors[1])

    passrate_exercise = bars_with_threshold(axes[2], labels[2], '10m',
        ['1h', '1h', '0', '15m', '1.5h', '1h', '1.5h', '1,5h', '0', '1h', '10m', '15m', '1h',
        '1,5h', '2h', '0', '0', '1h', '1.5h', '1h', '1.5h', '2h', '0', '0', '0', '1.5h', '10m',
        '10m', '1h', '0'], colors[2])

    passrate_sleep = bars_with_threshold(axes[3], labels[3], '7h',
        ['8h', '8h', '7h', '6h', '5h', '7h', '6h', '5h', '6,5h', '6h', '8h', '8h', '8h', '7,5h',
        '7h', '6,5h', '12h', '7,5h', '7,5h', '4h', '7h', '7h', '9h', '8h', '5h', '5,5h', '7h',
        '6h', '5,5h', '6h'], colors[3],
        ['0', '0', '0', '3h', '2h', '0', '0', '0', '3h', '3h', '0,5h', '0', '0', '0', '0', '0',
        '0', '0', '0', '3h', '0', '1h', '0', '0', '2.5h', '0', '2,5h', '0', '3,5h', '0'], colors[4])

    passrate_calories = bars_with_threshold(axes[4], labels[4], 2900,
        [3373, 2735, 3311, 3031, 2906, 2936, 3258, 2949, 2192, 2760, 2965, 2946, 2783, 3002, 2764,
        0, 3402, 2907, 3014, 3147, 3074, 2958, 0, 0, 2627, 3349, 3191, 3085, 3650, 0],
        colors[5], is_time=False, omit_zeros_in_avg=True)

    passrate_phone = bars_with_threshold(axes[5], labels[5], '3h 30m',
        ['1h 21m', '2h 23m', '2h 27m', '4h 28m', '3h 55m', '5h 25m', '2h 24m', '3h 8m', '2h 44m',
        '1h 23m', '2h 58m', '4h 22m', '3h 2m', '3h 34m', '4h 54m', '52m', '32m', '4h 10m',
        '3h 13m', '2h 56m', '3h 8m', '2h 33m', '59m', '1h 28m', '4h 1m', '2h 51m', '2h 38m',
        '3h 45m', '1h 57m', '1h 4m'], colors[6], threshold_is_min=False)

    plt.tight_layout()
    plt.savefig('summary_timeline.png')
    

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(polar=True))
    passrates = [passrate_projects, passrate_reading, passrate_exercise, passrate_sleep, passrate_calories,
                 passrate_phone, 0.50, 0.75, 0.70, 0.50]
    improvements = [9, -7, 12, 9, 47, -4, 0, 0, 0, 25]
    angles = np.linspace(0, 2 * np.pi, len(passrates), endpoint=False).tolist()
    angles += angles[:1]
    ax.fill(angles, passrates + passrates[:1], color=colors[4], alpha=0.25)
    ax.plot(angles, passrates + passrates[:1], color=colors[4], linewidth=2)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    for i, (label, value, improvement, angle) in enumerate(zip(labels, passrates, improvements, angles)):
        ha = 'right' if np.pi * 0.5 < angle < np.pi * 1.5 else 'left'
        ax.text(angle, 1.1, label, ha=ha, va='center', fontsize=12)
        text_kwargs = dict(ha='center', va='center', fontsize=12)
        text = ax.text(angle, value + 0.07, f"{value:.0%}", **text_kwargs)
        if improvement > 0:
            ax.annotate(f"\n(+{improvement}%)", xycoords=text, xy=(0.5, 0), color="green", **text_kwargs)
        if improvement < 0:
            ax.annotate(f"\n({improvement}%)", xycoords=text, xy=(0.5, 0), color="red", **text_kwargs)
    ax.text(0, 0, f"Overall\n{np.mean(passrates):.2%}", ha='center', va='center', fontsize=14, fontweight="bold")
    plt.savefig('summary_passrates.png')
