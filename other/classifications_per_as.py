#!/usr/bin/env python3

import json
from sys import argv

all_classifications = [
    'potentially_real',
    'honeypot_low_confidence',
    'honeypot_medium_confidence',
    'honeypot_high_confidence',
]

def print_as(asn, as_name, as_dict):
    all_sum = sum(as_dict.values())
    print(f"{f'AS{asn} ' if asn else ''}{as_name} - {all_sum} hosts")
    for cl in all_classifications:
        percentage = as_dict[cl] * 100 / all_sum
        print(f"    {cl.ljust(30)} {str(as_dict[cl]).rjust(5)}, {percentage:.1f}%")
    print()

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    ases = {}
    as_names = {}
    total_classifications = {c: 0 for c in all_classifications}
    
    for host in hosts:
        asn = host['asn']
        clas = host['classification']
        if asn in ases:
            as_dict = ases[asn]
        else:
            as_dict = ases[asn] = {c: 0 for c in all_classifications}
            as_names[asn] = host['as_name']
        as_dict[clas] += 1
        total_classifications[clas] += 1

    print_as(None, "Total", total_classifications)

    for asn in sorted(ases.keys(), key=lambda x: -sum(ases[x].values())):
        print_as(asn, as_names[asn], ases[asn])


if __name__ == '__main__':
    main()
