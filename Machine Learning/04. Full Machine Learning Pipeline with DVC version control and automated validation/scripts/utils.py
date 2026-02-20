import time
import shap
import mlflow
import numpy as np
import pandas as pd
import seaborn as sns
import gensim.downloader
from functools import wraps
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.base import BaseEstimator, TransformerMixin


class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.model = gensim.downloader.load('word2vec-google-news-300')
        # self.model = gensim.downloader.load('word2vec-ruscorpora-300')
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return np.array([self.get_sentence_vector(sentence) for sentence in X])
    
    def get_sentence_vector(self, sentence):
        vector_sum = np.zeros(self.model.vector_size)
        count = 0
        for word in sentence.split(' '):
            try:
                vector_sum += self.model[word]
                count += 1
            except: pass
        if count != 0: return vector_sum / count
        else: return vector_sum


def save_confusion_matrix(dataset: str, y: np.ndarray, y_pred: np.ndarray, name: str):
    cm = confusion_matrix(y, y_pred)
    cm_percent = cm.astype('float') / cm.sum()
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_percent, annot=True, fmt='.1%', cmap='Blues')
    plt.title(f'Confusion Matrix - {name.title()} Set')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.savefig(f'results_{dataset}/confusion_matrix_{name}.png')
    mlflow.log_artifact(f'results_{dataset}/confusion_matrix_{name}.png', 'confusion_matrices')


def save_shap_graph(dataset: str, pipeline: Pipeline, X: pd.DataFrame):
    x = pipeline['preprocessor'].transform(X)
    masker = shap.maskers.Independent(x, max_samples=100)
    explainer = shap.Explainer(pipeline['model'], masker)
    explanation = explainer(x)
    explanation = shap.Explanation(
        values=explanation.values, 
        base_values=explanation.base_values, 
        data=explanation.data, 
        feature_names=['rating', 'review_text_len', 'review_title_len', 'exclamations',
       'text', 'product_name', 'brand_name', 'is_recommended']
    )
    plt.figure(figsize=(8, 6))
    shap.plots.beeswarm(explanation[:,:,1])
    plt.tight_layout()
    plt.savefig(f'results_{dataset}/shap.png')
    mlflow.log_artifact(f'results/shap.png', 'shap')


def save_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        mlflow.log_metric(f'execution_time_seconds_{func.__name__}', end_time - start_time)
        return result
    return wrapper
