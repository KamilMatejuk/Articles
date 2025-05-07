import pandas as pd
from typing import Callable
import matplotlib.pyplot as plt


def show_nans(df: pd.DataFrame):
    attrs = [c for c in df.columns if c != 'class']
    nans = df[attrs].isna().sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.bar(nans.index, nans.values, color='#FF7400')
    ax.set_xticks(range(len(nans.index)))
    ax.set_xticklabels(nans.index, rotation=90)
    ax.set_xlim(-1, len(nans.index))
    fig.tight_layout()


def fill_nans(df: pd.DataFrame, fill: Callable):
    data = df.copy()
    attrs = [c for c in data.columns if c != 'class']
    fills = fill(data[attrs])
    data = data.fillna(fills)
    data = data[data['class'].notna()]
    return data


def show_boxplot(df: pd.DataFrame, iqr_ratio: float):
    attrs = [c for c in df.columns if c != 'class']
    fig, axes = plt.subplots(1, len(attrs), figsize=(12, 3), gridspec_kw={'wspace': 0})
    flierprops = dict(marker='x', markersize=3, markeredgecolor='#FF7400')
    for i, col in enumerate(attrs):
        df[[col]].boxplot(ax=axes[i], grid=False, whis=iqr_ratio, flierprops=flierprops, color='#FF7400')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')
        axes[i].tick_params(axis='x', labelrotation=90)
        axes[i].tick_params(axis='y', left=False, labelleft=False)
        for spine in ['top', 'right', 'left']:
            axes[i].spines[spine].set_visible(False)
    fig.tight_layout()


def remove_outliers(df: pd.DataFrame, iqr_ratio: float):
    data = df.copy()
    attrs = [c for c in data.columns if c != 'class']
    for col in attrs:
        q1 = data[col].quantile(0.25)
        q3 = data[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - iqr_ratio * iqr
        upper_bound = q3 + iqr_ratio * iqr
        data.loc[(data[col] < lower_bound) | (data[col] > upper_bound), col] = None
    return data
