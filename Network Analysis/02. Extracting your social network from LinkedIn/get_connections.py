import coordinates
from tools import run_instructions, remove_polish_chars

import os
import time
import pandas as pd


DOWNLOAD_PATH = '/home/kamil/Downloads'


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
        # save page with correct name
        run_instructions([
            'shortcut_{}_{}'.format('ctrl', 's'),
            'click_{}_{}'.format(*coordinates.SAVE_WINDOW),
            'type_{}'.format(filename),
            'press_{}'.format('enter'),
        ])
        time.sleep(3)
        # check if its correct page
        with open(f'{DOWNLOAD_PATH}/{filename}.html') as f:
            html_content = f.read()
        if 'No results found' in html_content or \
        'This one’s our fault' in html_content:
        # 'you might benefit from unlimited search' in html_content:
            # end for this pearson
            os.system(f'rm -r {DOWNLOAD_PATH}/{filename}*')
            break
        else:
            page += 1
            if page == 2:
                run_instructions([
                    'click_{}_{}'.format(*coordinates.BROWSER_LINK),
                    'press_{}'.format('end'),
                    'type_{}'.format(f'&page={page}'),
                    'press_{}'.format('enter'),
                ])
            else:
                run_instructions([
                    'click_{}_{}'.format(*coordinates.BROWSER_LINK),
                    'press_{}'.format('end'),
                    *('press_{}'.format('backspace') for _ in range(len(str(page-1)))),
                    'type_{}'.format(page),
                    'press_{}'.format('enter'),
                ])
            time.sleep(5)
    # repackage folder
    os.system(f'mkdir -p "results/{person}" && mv {DOWNLOAD_PATH}/* "results/{person}"')
            


if __name__ == '__main__':
    my_connections = pd.read_csv('Downloaded_1st_connections.csv', skiprows=3)
    names = sorted(set((my_connections['First Name'] + ' ' + my_connections['Last Name']).dropna()))
    for i, n in enumerate(names):
        if i < 23: continue
        extract_connections_of(n)
