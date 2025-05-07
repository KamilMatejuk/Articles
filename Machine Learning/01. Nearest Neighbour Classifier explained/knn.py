import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, KFold

import warnings
from sklearn.exceptions import UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


def knn(df: pd.DataFrame, kfold_cls=KFold, kf_kwargs=None, knn_kwargs=None):
    X = df.copy().drop('class', axis=1)
    y = df.copy()['class']
    kf = kfold_cls(**(kf_kwargs or {}))
    knn = KNeighborsClassifier(**(knn_kwargs or {}))
    accuracy = cross_val_score(knn, X, y, cv=kf, scoring='accuracy').mean()
    f1 = cross_val_score(knn, X, y, cv=kf, scoring='f1_macro').mean()
    precision = cross_val_score(knn, X, y, cv=kf, scoring='precision_macro').mean()
    recall = cross_val_score(knn, X, y, cv=kf, scoring='recall_macro').mean()
    return pd.DataFrame([[accuracy, f1, precision, recall]],
                        columns=['accuracy', 'f1', 'precision', 'recall'])
