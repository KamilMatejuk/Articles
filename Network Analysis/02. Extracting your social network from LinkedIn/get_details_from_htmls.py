import json
import glob
from bs4 import BeautifulSoup


def get_from_htmls(person: str):
    names = []
    for filename in sorted(glob.glob(f'results/{person}/*.html')):
        with open(filename) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        items = soup.select('.reusable-search__result-container')
        for li in items:
            name = li.select_one('.entity-result__title-text > a > span > span')
            if name is None: continue
            name = ''.join(name.contents).strip()
            print(name)
            names.append(name)
    with open(f'results/{person}.json', 'w+') as f:
        json.dump(names, f, ensure_ascii=False)
    
    
if __name__ == '__main__':
    get_from_htmls('Michał Kawa')

