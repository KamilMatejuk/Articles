import os
import tqdm
import zipfile
import requests
import pandas as pd
from scipy.io.arff import loadarff


URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00365/data.zip"
DIR = "data"


def load_dataset():
    files = [os.path.join(DIR, f'{y}year.arff') for y in range(1, 6)]
    if not all(os.path.exists(f) for f in files):
        print("Dataset files are missing.")
        download()
    df = pd.DataFrame()
    for f in files:
        df = pd.concat([df, pd.DataFrame(loadarff(f)[0])])
    df['class'] = df['class'].values.astype(int)
    df = df.reset_index(drop=True)
    return df
        

def download():
    print("Downloading...")
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        block_size = 8192 # 8KB
        with open('tmp.zip', 'wb') as f, tqdm.tqdm(total=total_size, unit='iB', unit_scale=True) as bar:
            for chunk in r.iter_content(chunk_size=block_size):
                f.write(chunk)
                bar.update(len(chunk))
    print("Unzipping...")
    with zipfile.ZipFile('tmp.zip', 'r') as zip_ref:
        zip_ref.extractall(DIR)
    print("Cleaning...")
    os.remove('tmp.zip')
