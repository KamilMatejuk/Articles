import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score, confusion_matrix

import warnings
from sklearn.exceptions import UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


def purity(y, pred):
    cm = confusion_matrix(y, pred)
    return cm.max(axis=1).sum() / cm.sum()


def run(df: pd.DataFrame, kwargs: dict, classifier: KMeans | DBSCAN):
    X = df.copy().drop('class', axis=1)
    y = df.copy()['class']
    kf = StratifiedKFold(n_splits=5)
    silhouette_scores, db_scores, rand_scores, purity_scores, clusters = [], [], [], [], []
    for train_idx, test_idx in kf.split(X, y):
        x_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        x_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
        if classifier == KMeans:
            model = classifier(random_state=42, **kwargs)
            model.fit(x_train)
            pred = model.predict(x_test)
        else:
            model = classifier(**kwargs)
            pred = model.fit_predict(x_test)
        # Silhouette and davies_bouldin require more than 1 cluster
        if len(set(pred)) > 1 and -1 not in pred:
            silhouette_scores.append(silhouette_score(x_test, pred))
            db_scores.append(davies_bouldin_score(x_test, pred))
        rand_scores.append(adjusted_rand_score(y_test, pred))
        purity_scores.append(purity(y_test, pred))
        clusters.append(len(set(pred)))
    return pd.DataFrame([[
        np.mean(silhouette_scores) if silhouette_scores else 0,
        np.mean(db_scores) if db_scores else 0,
        np.mean(rand_scores),
        np.mean(purity_scores),
        np.mean(clusters),
    ]], columns=['silhouette', 'davies_bouldin', 'rand', 'purity', 'clusters'])


def run_kmeans(df: pd.DataFrame, kwargs: dict): return run(df, kwargs, KMeans)
def run_dbscan(df: pd.DataFrame, kwargs: dict): return run(df, kwargs, DBSCAN)
