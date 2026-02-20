import sys
import yaml
from umap import UMAP
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.experimental import enable_halving_search_cv # for HalvingRandomSearchCV
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, HalvingRandomSearchCV, HalvingGridSearchCV

from utils import Word2VecVectorizer


with open('/app/params.yaml', 'r') as f:
    params = yaml.safe_load(f)
    
    DATASET_DIVISION_TEST_SIZE = params['dataset']['division_test_size']
    DATASET_DIVISION_RANDOM_STATE = params['dataset']['division_random_state']
    DATASET_DIVISION_STRATIFY = params['dataset']['division_stratify']
    
    TRAIN_USE_CROSS_VALIDATION = params['training']['use_cross_validation']
    TRAIN_USE_GRID_SEARCH = params['training']['use_grid_search']
    
    CREATE_SHAP_GRAPH = params['analysis']['create_shap_graph']


def get_selected_dataset_from_cmd() -> str:
    if len(sys.argv) > 1: SELECTED_DATASET = sys.argv[1]
    else: SELECTED_DATASET = 'sephora'
    assert SELECTED_DATASET in ['sephora', 'rotten_tomatoes'], \
        f'Incorrect dataset {SELECTED_DATASET}'
    return SELECTED_DATASET


def get_columns(dataset: str) -> tuple[list[str]|None, list[str]|None, list[str]|None, str]:
    if dataset == 'sephora':
        numerical = ['rating', 'review_text_len', 'review_title_len', 'exclamations']
        categorical = ['product_id', 'product_name', 'brand_name', 'is_recommended']
        text = ['review_text', 'review_title']
        y = 'LABEL-simple_rating'
        return numerical, categorical, text, y
    elif dataset == 'rotten_tomatoes':
        return None, None, ['text'], 'sentiment'
    else:
        raise ValueError(f'Incorrect dataset {dataset}')
        

def get_preprocessing_columns(dataset: str) -> list[str]:
    numerical, categorical, _, _ = get_columns(dataset)
    used_cols = []
    preprocess_columns = params['preprocessing']['columns']
    if preprocess_columns in ['numeric', 'all'] and categorical is not None: used_cols.extend(categorical)
    if preprocess_columns in ['numeric', 'all'] and numerical is not None: used_cols.extend(numerical)
    if preprocess_columns in ['text', 'all']: used_cols.append('text')
    return used_cols
    

def get_reducer() -> BaseEstimator | None:
    ''' Return selected dimentionality reducer instance'''
    reducer_selected = params['preprocessing']['dim_reduction']
    assert reducer_selected in ['none', 'pca', 'umap'], \
        f'Incorrect dimentionality reducer {reducer_selected}'
    dim = params['preprocessing']['dim_reduction_n']
    if reducer_selected == 'none': return None
    if reducer_selected == 'pca': return PCA(n_components=dim)
    if reducer_selected == 'umap': return UMAP(n_components=dim, random_state=42)


def get_vectorizer() -> BaseEstimator:
    ''' Return selected vectorizer instance'''
    vectorizer_selected = params['preprocessing']['vectorization']
    assert vectorizer_selected in ['bow', 'tf-idf', 'word2vec'], \
        f'Incorrect vectorizer {vectorizer_selected}'
    if vectorizer_selected == 'bow': return CountVectorizer()
    if vectorizer_selected == 'tf-idf': return TfidfVectorizer()
    if vectorizer_selected == 'word2vec': return Word2VecVectorizer()


def get_model() -> BaseEstimator:
    ''' Return selected model instance'''
    model_selected = params['model']['selected']
    assert model_selected in ['dummy', 'svm', 'random_forest'], \
        f'Incorrect model {model_selected}'
    kwargs = params['model'][model_selected]
    if model_selected == 'dummy': return DummyClassifier(**kwargs)
    if model_selected == 'svm': return SVC(**kwargs)
    if model_selected == 'random_forest': return RandomForestClassifier(**kwargs, random_state=42)


def get_grid_search_engine() -> tuple[BaseEstimator, dict]:
    ''' Return selected grid search egine class and kwargs dict'''
    assert TRAIN_USE_GRID_SEARCH, 'Grid search disabled'
    engine_selected = params['grid_search']['engine']
    assert engine_selected in ['RandomSearch', 'GridSearch', 'HalvingRandomSearch', 'HalvingGridSearch'], \
        f'Incorrect grid search engine {engine_selected}'
    p = get_grid_search_params()
    if engine_selected == 'RandomSearch': return RandomizedSearchCV, {'param_distributions': p, 'n_iter': 50}
    if engine_selected == 'GridSearch': return GridSearchCV, {'param_grid': p}
    if engine_selected == 'HalvingRandomSearch': return HalvingRandomSearchCV, {'param_distributions': p, 'factor': 3}
    if engine_selected == 'HalvingGridSearch': return HalvingGridSearchCV, {'param_grid': p, 'factor': 3}


def get_grid_search_params() -> dict:
    ''' Return params distributions for grid search for selected model'''
    assert TRAIN_USE_GRID_SEARCH, 'Grid search disabled'
    model_selected = params['model']['selected']
    assert model_selected in ['svm', 'random_forest'], \
        f'Incorrect model for grid search {model_selected}'
    par_dist = params['grid_search']['param_grid'][model_selected]
    return {f'model__{k}': v for k, v in par_dist.items()}


def extract_params_from_list(data: list, prefix: str = ''):
    pref = lambda i: f'{prefix}_{i}' if prefix else f'{i}'
    ps = {}
    for i, v in enumerate(data):
        if isinstance(v, list):
            ps.update(extract_params_from_list(v, pref(i)))
        elif isinstance(v, dict):
            ps.update(extract_params_from_dict(v, pref(i)))
        else:
            ps[pref(i)] = v
    return ps
            

def extract_params_from_dict(data: dict, prefix: str = ''):
    pref = lambda k: f'{prefix}_{k}' if prefix else f'{k}'
    ps = {}
    for k, v in data.items():
        if isinstance(v, dict):
            ps.update(extract_params_from_dict(v, pref(k)))
        elif isinstance(v, list):
            ps.update(extract_params_from_list(v, pref(k)))
        else:
            ps[pref(k)] = v
    return ps
            
        
def mlflow_log():
    import mlflow
    ps = extract_params_from_dict(params)
    # remove wrong model
    m = params['model']['selected']
    ps = {k: v for k, v in ps.items() if not (k.startswith('model_') and m not in k and 'selected' not in k)}
    ps = {k: v for k, v in ps.items() if not (k.startswith('grid_search_param_grid_') and m not in k)}
    if not TRAIN_USE_GRID_SEARCH: ps = {k: v for k, v in ps.items() if not k.startswith('grid_search')}
    mlflow.log_params(ps)
