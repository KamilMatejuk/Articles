import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


C_PASS = '#1fdd55'
C_FAIL = '#f6894c'
C_DEFAULT = 'lightblue'
C_SCALE = ['#c97d7d', '#d6b47d', '#7daf7d']
C_MACROS = ['blue', 'red', 'orange', 'black']


def set_style(ax: plt.Axes, index: pd.Series):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlim(index.min(), index.max())


def set_style_xticks(ax: plt.Axes, index: pd.Series):
    xticks = index[::7]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks.map(lambda x: x.strftime('%d.%m.%Y')), rotation=45, ha='right')


def show_passrate(ax: plt.Axes, values: pd.Series, passfail: pd.Series | None, index: pd.Series, time_format: bool):
    if passfail is None: colors = C_DEFAULT
    else: colors = [C_PASS if passed else C_FAIL for passed in passfail]
    ax.bar(index, values, color=colors, width=0.75)
    set_style(ax, index)
    set_style_xticks(ax, index)
    if time_format:
        if (max(values) // 60) > 1:
            ticks = range(1, int(max(values) // 60) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax.set_yticks([60 * i for i in ticks])
            ax.set_yticklabels([f'{i}h' for i in ticks])
        else:
            ticks = range(1, int(max(values) // 5) + 1)
            if len(ticks) > 7: ticks = ticks[::2]
            ax.set_yticks([5 * i for i in ticks])
            ax.set_yticklabels([f'{5*i}m' for i in ticks])

    if passfail is not None:
        y1 = values.max() * 0.55
        y2 = values.max() * 0.20
        x = index.max() + datetime.timedelta(days=7)
        pf = passfail.mean()
        avg = values.replace(0, np.nan).mean()
        if time_format:
            h = int(avg / 60)
            m = int(avg - h * 60)
            avg = ((f'{h}h' if h else '') + ' ' + (f'{m}m' if m else '')).strip()
        else: avg = f'{avg:.1f}'            
        ax.text(x, y1, s=f'average\n{avg}', ha='center', va='center', fontsize=12)
        ax.text(x, y2, s=f'passrate\n {pf:.1%}', ha='center', va='center', fontsize=12)


def create_graph_passrate(values_df: pd.DataFrame, passfail_df: pd.DataFrame, cols: list[str], labels: list[str], time_format: bool):
    fig, axes = plt.subplots(len(cols), 1, figsize=(10, 2 * len(cols) + 1), sharex=True)
    if len(cols) == 1: axes = [axes]
    for ax, col, label in zip(axes, cols, labels):
        show_passrate(ax, values_df[col], passfail_df[col] if col in passfail_df else None, values_df['date'], time_format=time_format)
        if len(axes) > 1: ax.set_title(label)
        else: print(label)
    fig.tight_layout()
    plt.show()
