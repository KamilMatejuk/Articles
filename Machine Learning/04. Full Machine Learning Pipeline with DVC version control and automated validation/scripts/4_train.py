import random; random.seed(42)
import numpy; numpy.random.seed(42)

import os
import json
import mlflow
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from utils import save_confusion_matrix, save_execution_time, save_shap_graph
from params import mlflow_log
from params import TRAIN_USE_CROSS_VALIDATION, TRAIN_USE_GRID_SEARCH
from params import CREATE_SHAP_GRAPH
from params import get_preprocessing_columns, get_reducer, get_vectorizer, get_model
from params import get_grid_search_engine
from params import get_selected_dataset_from_cmd, get_columns


def get_pipeline() -> Pipeline:
    numeric_steps = []
    text_steps = []
    # scale numerical
    numeric_steps.append(('scaler', StandardScaler()))
    # vectorize
    text_steps.append(('vectorizer', get_vectorizer()))
    # dimention reduction
    reducer = get_reducer()
    if reducer is not None:
        text_steps.append(('dim reducer', reducer))
    # combine all
    if COLUMNS_NUMERICAL is not None:
        preprocessor = ColumnTransformer(transformers=[
            ('num', Pipeline(steps=numeric_steps, verbose=True), COLUMNS_NUMERICAL),
            ('text', Pipeline(steps=text_steps, verbose=True), 'text')])
    else:
        preprocessor = ColumnTransformer(transformers=[
            ('text', Pipeline(steps=text_steps, verbose=True), 'text')])
    model = get_model()
    p = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)], verbose=True)
    print(f'Created pipeline {p}')
    return p


def get_x_y(filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(f'data/out_3_analyzed_{SELECTED_DATASET}/{filename}.csv', lineterminator='\n')
    x = df[get_preprocessing_columns(SELECTED_DATASET)]
    x['text'] = x['text'].fillna('')
    y = df[COLUMN_Y]
    return x, y


@save_execution_time
def train_grid_search(X: pd.DataFrame, y: pd.DataFrame, pipeline: Pipeline):
    engine, kwargs = get_grid_search_engine()
    print(f'Running grid search with {engine}')
    kwargs.update({'estimator': pipeline, 'cv': 5, 'verbose': 1})
    gs = engine(**kwargs)
    gs = gs.fit(X, y)
    print('Saving')
    data = {f'grid_search_best_{k}': v for k, v in gs.best_params_.items()}
    data['grid_search_best_accuracy'] = gs.best_score_
    data = {k: v if v is not None else 'None' for k, v in data.items()}
    with open(f'results_{SELECTED_DATASET}/metrics.json', 'w+') as f:
        json.dump(data, f)
    for k, v in data.items():
        mlflow.log_param(k, v)


@save_execution_time
def train_cross_validation(X: pd.DataFrame, y: pd.DataFrame, pipeline: Pipeline):
    print('Running training with cross validation 5-fold')
    cv_scores = cross_val_score(pipeline, X, y, cv=5)
    print('Saving')
    for i, cvs in enumerate(cv_scores):
        mlflow.log_metric(f'cross_validation_{i}', cvs)
    mlflow.log_metric('cross_validation_mean', cv_scores.mean())
    with open(f'results_{SELECTED_DATASET}/metrics.json', 'w+') as f:
        json.dump({
            'cross_validation_mean': cv_scores.mean(),
            'cross_validation_scores': [float(cvs) for cvs in cv_scores],
        }, f)


@save_execution_time
def train_regular_split(X_train: pd.DataFrame, y_train: pd.DataFrame,
                      X_test: pd.DataFrame, y_test: pd.DataFrame,
                      pipeline: Pipeline):
    print('Running training with regular split')
    print(f'Fitting pipeline')
    pipeline = pipeline.fit(X_train, y_train)
    print('Predicting on train')
    y_train_pred = pipeline.predict(X_train)
    print('Predicting on test')
    y_test_pred = pipeline.predict(X_test)
    print('Saving')
    accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average='weighted')
    recall = recall_score(y_test, y_test_pred, average='weighted')
    f1 = f1_score(y_test, y_test_pred, average='weighted')
    save_confusion_matrix(SELECTED_DATASET, y_train, y_train_pred, 'train')
    save_confusion_matrix(SELECTED_DATASET, y_test, y_test_pred, 'test')
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_metric('precision', precision)
    mlflow.log_metric('recall', recall)
    mlflow.log_metric('f1_score', f1)
    with open(f'results_{SELECTED_DATASET}/metrics.json', 'w+') as f:
        json.dump({
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
        }, f)


def train_and_evaluate():
    mlflow.start_run()
    name = os.environ.get('DVC_EXP_NAME')
    if name is not None:
        mlflow.set_tag('mlflow.runName', f'{name}_{SELECTED_DATASET}')
    mlflow_log()
    mlflow.log_param('dataset', SELECTED_DATASET)
    X_train, y_train = get_x_y('train')
    X_test, y_test = get_x_y('test')
    pipeline = get_pipeline()
    if TRAIN_USE_GRID_SEARCH:
        train_grid_search(X_train, y_train, pipeline)
    elif TRAIN_USE_CROSS_VALIDATION:
        train_cross_validation(X_train, y_train, pipeline)
    else:
        train_regular_split(X_train, y_train, X_test, y_test, pipeline)

    if CREATE_SHAP_GRAPH:
        save_shap_graph(SELECTED_DATASET, pipeline, X_test)
    mlflow.end_run()


if __name__ == '__main__':
    mlflow.set_tracking_uri('http://127.0.0.1:5000')
    SELECTED_DATASET = get_selected_dataset_from_cmd()
    COLUMNS_NUMERICAL, COLUMNS_CATEGORICAL, COLUMNS_TEXT, COLUMN_Y = get_columns(SELECTED_DATASET)
    os.makedirs(f'results_{SELECTED_DATASET}', exist_ok=True)
    train_and_evaluate()
