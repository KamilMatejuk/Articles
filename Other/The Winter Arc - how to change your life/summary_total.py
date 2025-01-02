import numpy as np
import matplotlib.pyplot as plt

from summary import bars_with_threshold

if __name__ == '__main__':
    rows = 6
    colors = [plt.cm.winter(i) for i in np.linspace(0, 1, rows + 1)]
    
    labels = ['Side projects', 'Reading', 'Exercise', 'Sleep', 'Calories', 'Phone usage',
              'Articles', 'Posts', 'Gym', 'Shoulder raises', 'Alcohol']

    fig, axes = plt.subplots(rows, 1, figsize=(12, 2 * rows))

    passrate_projects = bars_with_threshold(axes[0], labels[0], '15m',
        ['15m', '1h', '1h', '30m', '2h', '2h', '3h', '0', '0', '2h', '30m', '5h', '2,5h', '0',
        '0', '15m', '3h', '0', '0', '0', '0', '0', '1h', '1h', '2.5h', '3h', '2h', '5m', '0',
        '0', '30m', '30m', '3h', '2h', '30m', '1h 45m', '2,5h', '4h', '3h', '4h', '0', '2h', '1.5h', '0', '0',
        '1,5h', '0', '0', '0', '0.5h', '15m', '2h', '2.5h', '0', '0', '0,5h', '2h', '15m', '4,5h',
        '15m', '0', '2.5h', '0', '1,5h', '2,5h', '30m', '0', '0', '15m', '2.5h', '2h', '3h', '2h', '1,5h', '0', '0', '30m', '30m', '2h', '30m', '0', '0', '3h', '4h', '15m', '15m', '0', '5h', '3,5h', '5h', '1,5h', '1,5h'], colors[0])

    passrate_reading = bars_with_threshold(axes[1], labels[1], '5m',
        ['20m', '15m', '15m', '25m', '10m', '15m', '20m', '5m', '15m', '30m', '15m', '20m', '10m',
        '10m', '5m', '0', '15m', '20m', '0', '0', '15m', '15m', '15m', '0', '0', '15m', '20m',
        '15m', '0', '0', '20m', '25m', '50m', '0', '30m', '35m', '0', '0', '10m', '0', '0', '10m', '25m', '10m', '0', '0',
        '0', '10m', '0', '10m', '10m', '20m', '5m', '15m', '5m', '20m', '10m', '20m', '10m', '10m',
        '5m', '5m', '0', '25m', '15m', '5m', '5m', '5m', '15m', '0', '10m', '10m', '15m', '0', '5m', '30m', '10m', '15m', '15m', '0', '0', '0', '15m', '45m', '5m', '1h', '0', '0', '10m', '0', '5m', '10m'], colors[1])

    passrate_exercise = bars_with_threshold(axes[2], labels[2], '10m',
        ['2.5h', '20m', '1.5h', '1h', '0', '3h', '0', '3h', '5m', '0', '2.5h', '20m', '0', '1h',
        '1.5h', '1h', '0', '2h', '4h', '0', '0', '2.5h', '10m', '1.5h', '1h', '0', '1h', '0',
        '0', '20m', '0', '1h', '1h', '0', '15m', '1.5h', '1h', '1.5h', '1,5h', '0', '1h', '10m', '15m', '1h',
        '1,5h', '2h', '0', '0', '1h', '1.5h', '1h', '1.5h', '2h', '0', '0', '0', '1.5h', '10m',
        '10m', '1h', '0', '0', '1h', '1.5h', '1h', '0', '2h', '0', '0', '1h', '1.5h', '1h', '0', '1h', '0', '0', '0', '2.5h', '10m', '1.5h', '0', '0', '0', '10m', '0', '0', '0', '0', '0', '0', '0', '15m'], colors[2])

    passrate_sleep = bars_with_threshold(axes[3], labels[3], '7h',
        ['7h', '6h', '7,5h', '5h', '6h', '10h', '6.5h', '5,5h', '6,5h', '7,5h', '5,5h', '9h',
        '7,5h', '6h', '6,5h', '9h', '7h', '7h', '7,5h', '11h', '5h', '5,5h', '7h', '7h', '6.5h',
        '7h', '8h', '8h', '3.5h', '10h', '6h', '8h', '8h', '7h', '6h', '5h', '7h', '6h', '5h', '6,5h', '6h', '8h', '8h', '8h', '7,5h',
        '7h', '6,5h', '12h', '7,5h', '7,5h', '4h', '7h', '7h', '9h', '8h', '5h', '5,5h', '7h',
        '6h', '5,5h', '6h', '8h', '5,5h', '6,5h', '6,5h', '6,5h', '4,5h', '10h', '11h', '5h', '6h', '7h', '6h', '5,5h', '3h', '7h', '6,5h', '5,5h', '6h', '4,5h', '9,5h', '0h', '9h', '6,5h', '8h', '3,5h', '10h', '11h', '4,5h', '6,5h', '4,5h', '5h'], colors[3],
        ['0', '0', '0', '3h', '0', '0', '2h', '0', '0', '3h', '1,5h', '3h', '0', '0', '0', '0', '0',
        '2h', '0', '2h', '3h', '0', '0', '1h', '0', '4h', '0', '2h', '4h', '2h', '0', '0', '0', '0', '3h', '2h', '0', '0', '0', '3h', '3h', '0,5h', '0', '0', '0', '0', '0',
        '0', '0', '0', '3h', '0', '1h', '0', '0', '2.5h', '0', '2,5h', '0', '3,5h', '0', '0', '2h', '2h', '0', '3h', '0', '0', '0', '0', '0', '0', '3h', '0', '2h', '2h', '2h', '0', '3h', '0', '1h', '6h', '0', '0', '0', '1h', '0', '0', '5h', '3h', '0', '3h'], colors[4])

    passrate_calories = bars_with_threshold(axes[4], labels[4], 2900,
        [1826, 3179, 2783, 2145, 2361, 2222, 2325, 1796, 2860, 2789, 2537, 3148, 2458, 2756, 2224,
        2898, 2629, 2131, 0, 1487, 2349, 2822, 3640, 2465, 3578, 2306, 3016, 3233, 2395, 2480, 3373, 2735, 3311, 3031, 2906, 2936, 3258, 2949, 2192, 2760, 2965, 2946, 2783, 3002, 2764,
        0, 3402, 2907, 3014, 3147, 3074, 2958, 0, 0, 2627, 3349, 3191, 3085, 3650, 0, 2242, 2921, 2904, 2943, 2918, 2998, 2310, 2456, 2975, 3142, 2932, 2913, 2530, 2377, 2640, 3043, 2920, 2911, 1149, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        colors[5], is_time=False, omit_zeros_in_avg=True)

    passrate_phone = bars_with_threshold(axes[5], labels[5], '3h 30m',
        ['3h 32m', '5h 19m', '3h 11m', '4h 30m', '1h 4m', '2h 29m', '3h 17m', '4h 55m', '6h 8m',
        '4h 26m', '3h 57m', '54m', '2h 36m', '4h 11m', '3h 25m', '3h 17m', '3h 48m', '3h 25m',
        '1h 13m', '1h 4m', '4h 26m', '3h 57m', '3h 31m', '2h 19m', '3h 32m', '45m', '1h 34m',
        '3h 6m', '3h 31m', '2h 57m', '4h 2m', '1h 21m', '2h 23m', '2h 27m', '4h 28m', '3h 55m', '5h 25m', '2h 24m', '3h 8m', '2h 44m',
        '1h 23m', '2h 58m', '4h 22m', '3h 2m', '3h 34m', '4h 54m', '52m', '32m', '4h 10m',
        '3h 13m', '2h 56m', '3h 8m', '2h 33m', '59m', '1h 28m', '4h 1m', '2h 51m', '2h 38m',
        '3h 45m', '1h 57m', '1h 4m', '2h 12m', '2h 59m', '2h 37m', '4h 30m', '3h 10m', '2h 30m', '1h', '1h 53m', '4h 11m', '3h 20m', '3h 6m', '2h 53m', '3h 1m', '2h 9m', '1h 53m', '4h 36m', '3h 4m', '1h 49m', '3h 30m', '2h 3m', '1h 54m', '1h 40m', '5h', '55m', '2h 31m', '2h 4m', '2h 10m', '4h 9m', '2h 46m', '3h 45m', '3h 29m'], colors[6], threshold_is_min=False)

    xlabels = [1] + list(range(10, 92, 10)) + [92]
    for ax in axes:
        ax.set_xticks([x-1 for x in xlabels], xlabels)
    plt.tight_layout()
    plt.savefig('summary_total_timeline.png')
    

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(polar=True))
    passrates_oct = [0.61, 0.77, 0.61, 0.71, 0.20, 0.74, 0.50, 0.50, 0.75, 0.30, 0.25]
    passrates_nov = [0.70, 0.70, 0.73, 0.80, 0.67, 0.70, 0.50, 0.50, 0.75, 0.70, 0.50]
    passrates_dec = [0.74, 0.71, 0.42, 0.61, 0.63, 0.81, 1.00, 0.80, 0.40, 0.81, 0.60]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    passrates = [passrates_oct, passrates_nov, passrates_dec]
    cs = [colors[i] for i in [0, 3, 6]]
    months = ['Oct', 'Nov', 'Dec']
    for pr, c, l in zip(passrates, cs, months):
        ax.fill(angles, pr + pr[:1], color=c, alpha=0.25, label=l)
        ax.plot(angles, pr + pr[:1], color=c, linewidth=1)
        if l == 'Oct':
            a = angles[:7] + angles[8:9] + angles[10:]
            pr = pr[:7] + pr[8:9] + pr[10:]
            ax.scatter(a, pr + pr[:1], color=c)
        if l == 'Nov':
            a = angles[:7] + angles[8:]
            pr = pr[:7] + pr[8:]
            ax.scatter(a, pr + pr[:1], color=c)
        if l == 'Dec':
            ax.scatter(angles, pr + pr[:1], color=c)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    for i, (label, angle) in enumerate(zip(labels, angles)):
        ha = 'right' if np.pi * 0.5 < angle < np.pi * 1.5 else 'left'
        ax.text(angle, 1.1, label, ha=ha, va='center', fontsize=12)
    ax.legend()
    plt.savefig('summary_total_passrates.png')
