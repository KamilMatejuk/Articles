import os
import pandas as pd
from sklearn.model_selection import train_test_split


from params import DATASET_DIVISION_RANDOM_STATE
from params import DATASET_DIVISION_TEST_SIZE
from params import DATASET_DIVISION_STRATIFY
from params import get_selected_dataset_from_cmd, get_columns


def _resize(df: pd.DataFrame, cls_size: int):
    df = df.groupby(COLUMN_Y).apply(lambda group: group.head(cls_size))
    df = df.reset_index(drop=True)
    df[COLUMN_Y] = df[COLUMN_Y].apply(str)
    return df
    
def split():
    df = pd.read_csv(f'data/out_1_preprocessed_{SELECTED_DATASET}/data.csv', lineterminator='\n')
    if not DATASET_DIVISION_STRATIFY: stratify = None
    else: stratify = df[COLUMN_Y]
    train, test = train_test_split(df, stratify=stratify,
                                   test_size=DATASET_DIVISION_TEST_SIZE,
                                   random_state=DATASET_DIVISION_RANDOM_STATE)
    train = _resize(train, 5_000) # 875_528 -> 81_000
    test = _resize(test, 1_000) # 218_883 -> 21_000
    train.to_csv(f'data/out_2_split_{SELECTED_DATASET}/train.csv', index=False, lineterminator='\n')
    test.to_csv(f'data/out_2_split_{SELECTED_DATASET}/test.csv', index=False, lineterminator='\n')
    

if __name__ == '__main__':
    SELECTED_DATASET = get_selected_dataset_from_cmd()
    COLUMN_Y = get_columns(SELECTED_DATASET)[3]
    os.makedirs(f'data/out_2_split_{SELECTED_DATASET}', exist_ok=True)
    split()
    
