import coordinates
from tools import run_instructions, remove_polish_chars
from get_details_from_htmls import get_from_htmls

import os
import re
import time
import glob
import pyperclip
import pandas as pd


DOWNLOAD_PATH = '/home/kamil/Downloads'
FIRST_CONNECTIONS = 'Downloaded_1st_connections.csv'


def get_max_downloaded_page():
    page = 0
    for file in glob.glob(f'{DOWNLOAD_PATH}/*.html'):
        p = int(file.split('.')[-2].split('_')[-1])
        if p > page: page = p
    return page
    

def extract_connections_of(person: str):
    if os.path.exists(f"results/{person}"):
        print(f'SKIPPING {person}')
    # enter person
    run_instructions([
        'click_{}_{}'.format(*coordinates.DROPDOWN),
        'click_{}_{}'.format(*coordinates.SEARCH_FIELD),
        'type_{}'.format(person),
        'click_{}_{}'.format(*coordinates.CHOOSE_FIRST_FOUND),
        'click_{}_{}'.format(*coordinates.SHOW_RESULTS),
    ])
    # go through pages
    page = 1
    while True:
        print(f'{person} PAGE {page}'.upper())
        filename = remove_polish_chars(f'{person}_{page}'.lower().replace(' ', '_'))
        path = f'{DOWNLOAD_PATH}/{filename}.html'
        # save page with correct name
        if not os.path.exists(path):
            time.sleep(5)
            run_instructions([
                'shortcut_{}_{}'.format('ctrl', 's'),
                'click_{}_{}'.format(*coordinates.SAVE_WINDOW),
                'type_{}'.format(filename),
                'press_{}'.format('enter'),
            ])
            time.sleep(5)
        else:
            print('skip download')
            time.sleep(1)
        # check if its correct page
        with open(path) as f:
            html_content = f.read()
        if 'No results found' in html_content or \
        'This one’s our fault' in html_content:
        # 'you might benefit from unlimited search' in html_content:
            # end for this pearson
            os.system(f'rm -r {DOWNLOAD_PATH}/{filename}*')
            break
        else:
            page = get_max_downloaded_page() + 1
            run_instructions(['shortcut_ctrl_l', 'shortcut_ctrl_c'])
            url = pyperclip.paste().strip()
            if m := re.search('page=([0-9]+)', url):
                url = url.replace(f'page={m.group(1)}', f'page={page}')
            else: url += f'&page={page}'
            pyperclip.copy(url)
            run_instructions(['shortcut_ctrl_v', 'press_enter'])
            time.sleep(3)


if __name__ == '__main__':
    my_connections = pd.read_csv(FIRST_CONNECTIONS, skiprows=3)
    names = sorted(set((my_connections['First Name'] + ' ' + my_connections['Last Name']).dropna()))
    for i, n in enumerate(names):
        if os.path.exists(f'results/{n}.json'):
            print(f'skip {n}')
            continue
        extract_connections_of(n)
        person_filename = remove_polish_chars(n.lower().replace(' ', '_'))
        assert os.system(f'mkdir -p "results/{n}" && mv {DOWNLOAD_PATH}/{person_filename}* "results/{n}"') == 0
        get_from_htmls(n)
