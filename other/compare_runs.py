#!/usr/bin/env python3

import json
from sys import argv

from tabulate import tabulate

def split_honeypots(hosts):
    honeypot_classifications = ['honeypot_medium_confidence', 'honeypot_high_confidence']
    real_classifications = ['potentially_real']
    real = set()
    honeypot = set()
    for h in hosts:
        is_real = h['classification'] in real_classifications
        is_honeypot = h['classification'] in honeypot_classifications

        ip = h['ip']

        if is_real:
            assert is_honeypot == False
            assert ip not in honeypot
            real.add(ip)
        else:
            assert is_honeypot == True
            assert ip not in real
            honeypot.add(ip)
    return real, honeypot


def main():
    filename1 = argv[1]
    filename2 = argv[2]
    file1 = open(filename1)
    file2 = open(filename2)
    hosts1 = json.load(file1)
    hosts2 = json.load(file2)
    out1except2 = argv[3]
    out2except1 = argv[4]

    real1, honeypot1 = split_honeypots(hosts1)
    real2, honeypot2 = split_honeypots(hosts2)

    print('Total 1:', len(real1) + len(honeypot1))
    print('Real 1:', len(real1))
    print('Honeypot 1:', len(honeypot1))
    print()
    print('Total 2:', len(real2) + len(honeypot2))
    print('Real 2:', len(real2))
    print('Honeypot 2:', len(honeypot2))
    print()
    print('Real intersection:', len(real1.intersection(real2)))
    print('Honeypot intersection:', len(honeypot1.intersection(honeypot2)))
    print()
    print('Real 1 but not in 2:', len(real1 - real2))
    print('Honeypot 1 but not in 2:', len(honeypot1 - honeypot2))
    print()
    print('Real 2 but not in 1:', len(real2 - real1))
    print('Honeypot 2 but not in 1:', len(honeypot2 - honeypot1))
    print()

    all1 = real1 | honeypot1
    all2 = real2 | honeypot2

    with open(out1except2, "w") as file:
        file.write(json.dumps(list(h for h in hosts1 if h['ip'] not in all2), indent=4))
    with open(out2except1, "w") as file:
        file.write(json.dumps(list(h for h in hosts2 if h['ip'] not in all1), indent=4))




if __name__ == '__main__':
    main()
