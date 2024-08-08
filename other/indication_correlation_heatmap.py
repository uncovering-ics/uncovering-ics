#!/usr/bin/env python3

import json
from sys import argv

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    filename = argv[1]
    output_file = argv[2]
    file = open(filename)
    hosts = json.load(file)

    all_indications = set()
    host_indications = []
    for host in hosts:
        ind = set(host['indications'])
        all_indications.update(ind)
        host_indications.append(ind)
    
    indications_arr = list(sorted(x for x in all_indications))

    print(indications_arr)

    indications_dict = {ind: [] for ind in indications_arr}
    for host_ind in host_indications:
        for ind in indications_arr:
            indications_dict[ind].append(1 if ind in host_ind else 0)
    
    # print(indications_dict)
    
    df = pd.DataFrame(indications_dict)
    sns.set(rc = {'figure.figsize':(10,10)})
    sns.set(font_scale=2.3)
    sns.heatmap(df.corr(), annot=True, cmap="RdBu", vmin=-1, vmax=1, fmt='.1f', cbar=False)
    plt.xticks(rotation=45, ha='right')
    plt.savefig(output_file, bbox_inches='tight')


if __name__ == '__main__':
    main()
