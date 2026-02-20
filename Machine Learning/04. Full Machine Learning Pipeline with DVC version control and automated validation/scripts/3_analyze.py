import os
import re
import spacy
import pandas as pd

from params import get_selected_dataset_from_cmd, get_columns


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    if SELECTED_DATASET == 'sephora':
        df = df.dropna(subset=['is_recommended'])
    df = df.dropna(subset=COLUMNS_TEXT, how='all')
    for c in COLUMNS_TEXT:
        df[c] = df[c].fillna('').astype(str)
    return df


def code_categoric(df: pd.Series) -> pd.Series:
    return df.map({v: i for i, v in enumerate(sorted(df.unique()))})


def clean_text(df: pd.Series) -> pd.Series:
    # remove stopwords
    stopwords = set(pd.read_csv('/app/data/in/stopwords.csv', header=None)[0].values)
    df = df.apply(lambda x: ' '.join(xi for xi in x.split(' ') if xi not in stopwords))
    # remove puctuation
    df = df.apply(lambda x: re.sub(r'[^\w\s]', '', x))
    return df


def drop_non_emotional(df: pd.Series) -> pd.Series:
    nlp = spacy.load("/app/data/en_core_web_sm/en_core_web_sm-3.7.1")
    return df.apply(lambda text: ' '.join(token.text for token in nlp(text) if token.sentiment is not None))
    
    
def analyze(filename: str):
    df = pd.read_csv(f'data/out_2_split_{SELECTED_DATASET}/{filename}.csv', lineterminator='\n')
    df[COLUMN_Y] = df[COLUMN_Y].apply(str)
    # fill NaNs
    df = fill_missing_values(df)
    # clean text
    _combine_text = lambda row: ' '.join(str(v) for k, v in row.items() if k in COLUMNS_TEXT)
    df['text'] = df.apply(_combine_text, axis=1)
    df['text'] = clean_text(df['text'])
    df = df.drop(list(filter(lambda c: c != 'text', COLUMNS_TEXT)), axis=1)
    # remove nonemotional text components
    df['text'] = drop_non_emotional(df['text'])
    # code categorical
    cat = (COLUMNS_CATEGORICAL if COLUMNS_CATEGORICAL is not None else []) + [COLUMN_Y]
    for c in cat:
        df[c] = code_categoric(df[c])
    df.to_csv(f'data/out_3_analyzed_{SELECTED_DATASET}/{filename}.csv', index=False, lineterminator='\n')
    

if __name__ == '__main__':
    SELECTED_DATASET = get_selected_dataset_from_cmd()
    _, COLUMNS_CATEGORICAL, COLUMNS_TEXT, COLUMN_Y = get_columns(SELECTED_DATASET)
    os.makedirs(f'data/out_3_analyzed_{SELECTED_DATASET}', exist_ok=True)
    analyze('train')
    analyze('test')
