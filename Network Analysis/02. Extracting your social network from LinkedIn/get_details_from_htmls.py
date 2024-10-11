import json
import glob
from bs4 import BeautifulSoup


def get_from_htmls(person: str):
    names = set()
    for filename in sorted(glob.glob(f'results/{person}/*.html')):
        with open(filename) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        items = soup.select('.reusable-search__result-container')
        for li in items:
            name = li.select_one('.entity-result__title-text > a > span > span')
            if name is None: continue
            name = ''.join(name.get_text(strip=True)).strip()
            names.add(name)
    if len(names) == 0: return
    with open(f'results/{person}.json', 'w+') as f:
        json.dump(list(names), f, ensure_ascii=False)

