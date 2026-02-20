import os
import sys
import glob
import pandas as pd

from params import get_selected_dataset_from_cmd


def get_reviews() -> pd.DataFrame:
    reviews = []
    for file in glob.glob('data/in/reviews*.csv'):
        reviews.append(pd.read_csv(file, lineterminator='\n', usecols=[
        'LABEL-simple_rating', 'is_recommended', 'review_text', 'review_title', 'product_id']))
    return pd.concat(reviews)


def get_products() -> pd.DataFrame:
    return pd.read_csv('data/in/product_info.csv', lineterminator='\n', usecols=[
        'product_id', 'product_name', 'brand_name', 'rating'])


def _calc_len(x):
    try: return len(x)
    except: return 0


def _calc_exclamations(x1, x2):
    try: x1 = x1.count('!')
    except: x1 = 0
    try: x2 = x2.count('!')
    except: x2 = 0
    return x1 + x2


if __name__ == '__main__':
    SELECTED_DATASET = get_selected_dataset_from_cmd()
    os.makedirs(f'data/out_1_preprocessed_{SELECTED_DATASET}', exist_ok=True)
    if SELECTED_DATASET == 'sephora':
        df = pd.merge(get_products(), get_reviews(), how='inner', on='product_id')
        df['review_text_len'] = df['review_text'].apply(_calc_len)
        df['review_title_len'] = df['review_title'].apply(_calc_len)
        df['exclamations'] = df.apply(lambda row: _calc_exclamations(row['review_text'], row['review_title']), axis=1)
        df.to_csv(f'data/out_1_preprocessed_{SELECTED_DATASET}/data.csv', index=False, lineterminator='\n')
    elif SELECTED_DATASET == 'rotten_tomatoes':
        data = []
        with open('data/in/rt-polarity.pos', 'r', encoding='utf-8', errors='ignore') as f:
            data.extend([(line.strip(), 1) for line in f.readlines()])
        with open('data/in/rt-polarity.neg', 'r', encoding='utf-8', errors='ignore') as f:
            data.extend([(line.strip(), 0) for line in f.readlines()])
        df = pd.DataFrame(data, columns=['text', 'sentiment'])
        df.to_csv(f'data/out_1_preprocessed_{SELECTED_DATASET}/data.csv', index=False, lineterminator='\n')
    else: raise ValueError(f'Unknown dataset {SELECTED_DATASET}')
