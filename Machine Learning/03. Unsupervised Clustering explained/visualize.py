import numpy as np
import pandas as pd
from umap import UMAP
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN


def rotate_y(points, angle_degrees):
    angle_radians = np.deg2rad(angle_degrees)
    cos_a = np.cos(angle_radians)
    sin_a = np.sin(angle_radians)
    rotation_matrix = np.array([
        [ cos_a, 0, -sin_a],
        [     0, 1,      0],
        [ sin_a, 0,  cos_a]
    ])
    return points @ rotation_matrix.T


def show_3d(x: pd.DataFrame, y: pd.Series, ax: plt.Axes):
    ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=y, cmap='viridis', s=10)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]: axis.set_tick_params(color='white', labelcolor='white')


def show(df: pd.DataFrame, kwargs: dict, classifier: KMeans | DBSCAN):
    X = df.copy().drop('class', axis=1)
    if classifier == KMeans:
        kwargs['random_state'] = 42
    model = classifier(**kwargs)
    pred = model.fit_predict(X)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    X = PCA(n_components=3).fit_transform(X)
    show_3d(X, pred, ax)
    plt.show()


def show_kmeans(df: pd.DataFrame, kwargs: dict): return show(df, kwargs, KMeans)
def show_dbscan(df: pd.DataFrame, kwargs: dict): return show(df, kwargs, DBSCAN)


def compare_pca_umap(df: pd.DataFrame):
    X = df.copy().drop('class', axis=1)
    pca_result = PCA(n_components=3).fit_transform(X)
    umap_result = rotate_y(UMAP(n_components=3).fit_transform(X), 60)

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(121, projection='3d')
    show_3d(pca_result, df['class'], ax)
    ax.set_title('PCA')
    
    ax = fig.add_subplot(122, projection='3d')
    show_3d(umap_result, df['class'], ax)
    ax.set_title('UMAP')
    plt.show()
