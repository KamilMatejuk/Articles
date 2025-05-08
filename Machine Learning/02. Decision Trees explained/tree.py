import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate, StratifiedKFold

import warnings
from sklearn.exceptions import UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


def tree(df: pd.DataFrame, kwargs=None):
    X = df.copy().drop('class', axis=1)
    y = df.copy()['class']
    kf = StratifiedKFold(n_splits=5)
    classifier = DecisionTreeClassifier(random_state=42, **(kwargs or {}))
    scores = cross_validate(classifier, X, y, cv=kf, return_train_score=False,
        scoring=['accuracy', 'f1_macro', 'precision_macro', 'recall_macro'])
    metrics = pd.DataFrame([[
        scores['test_accuracy'].mean(),
        scores['test_f1_macro'].mean(),
        scores['test_precision_macro'].mean(),
        scores['test_recall_macro'].mean()
    ]], columns=['accuracy', 'f1', 'precision', 'recall'])
    classifier.fit(X, y)
    return metrics, classifier


def test(df: pd.DataFrame, keyword: str, values: list, other_kwargs: dict):
    combined = pd.DataFrame()
    for v in values:
        res, _ = tree(df, { keyword: v, **other_kwargs })
        res[keyword] = v
        combined = pd.concat([combined, res])
    combined.index = combined[keyword]
    combined.drop(columns=[keyword], inplace=True)
    plt.figure(figsize=(6, len(values)))
    sns.heatmap(combined, cmap="RdYlGn", vmin=0, vmax=1, annot=True, fmt=".0%")
    plt.show()
