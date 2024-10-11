from get_connections import FIRST_CONNECTIONS

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import glob
import json
import csv


if __name__ == '__main__':
    edges = set()
    # first
    my_connections = pd.read_csv(FIRST_CONNECTIONS, skiprows=3)
    names = set((my_connections['First Name'] + ' ' + my_connections['Last Name']).dropna())
    for n in names:
        edges.add(('me', n))
    # second+
    for filename in glob.glob(f'results/*.json'):
        with open(filename) as f:
            for name in json.load(f):
                edges.add((filename[8:-5], name))
    # save
    with open('network_edges.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['Person A', 'Person B'])
        for a, b in edges:
            writer.writerow([a, b])
