#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt

def main():
    filename = argv[1]
    output_file = argv[2]
    file = open(filename)
    hosts = json.load(file)

    all_classifications = [
        'classification_potentially_real',
        'classification_likely_honeypot',
        'classification_honeypot',
    ]

    classifications = {c: 0 for c in all_classifications}
    
    for host in hosts:
        clas = next(filter(lambda i: i in all_classifications, host['indications']))
        classifications[clas] += 1

    print([c.replace('classification_', '') for c in all_classifications])
    print([classifications[c] for c in all_classifications])

    plt.rc('font', size=15)
    plt.barh([c.replace('classification_', '') for c in all_classifications],
             [classifications[c] for c in all_classifications],
             color=['cornflowerblue', 'lightcoral', 'firebrick'])
    plt.xlabel('Number of hosts')
    plt.ylabel('Classification')
    plt.savefig(output_file, bbox_inches='tight')
    
    


if __name__ == '__main__':
    main()
