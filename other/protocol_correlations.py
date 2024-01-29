#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    host_protocols = dict()
    protocol_hosts = dict()
    for host in hosts:
        ip = host['ip']
        protocol = host['protocol']
        if protocol not in protocol_hosts:
            protocol_hosts[protocol] = set()
        protocol_hosts[protocol].add(ip)

        if ip not in host_protocols:
            host_protocols[ip] = set(protocol)
        host_protocols[ip].add(protocol)

    n_all_hosts = len(host_protocols)
    all_protocols = sorted(protocol_hosts)

    for p in all_protocols:
        h = protocol_hosts[p]
        probability = 100 * len(h) / n_all_hosts
        print(f'{p}: {len(h)}')
        print(f'  P({p}) = {probability:.1f}%')

    print()

    for p1i in range(len(all_protocols)):
        p1 = all_protocols[p1i]
        for p2 in all_protocols[(p1i+1):]:
            pred = f'{p1} and {p2}'
            h = protocol_hosts[p1] & protocol_hosts[p2]
            probability = 100 * len(h) / n_all_hosts
            probability_cond_p1 = 100 * len(h) / (len(protocol_hosts[p1]))
            probability_cond_p2 = 100 * len(h) / (len(protocol_hosts[p2]))
            print(f'{pred}: {len(h)}')
            if len(h) > 0:
                print(f'  P({pred}) = {probability:.1f}%')
                print(f'  P({p2} | {p1}) = {probability_cond_p1:.1f}%')
                print(f'  P({p1} | {p2}) = {probability_cond_p2:.1f}%')


if __name__ == '__main__':
    main()
