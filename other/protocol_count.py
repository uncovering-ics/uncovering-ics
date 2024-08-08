#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def main():
    filename = argv[1]
    plot_type = argv[2]
    assert plot_type in ['honeypot', 'real']
    output_file = argv[3]
    file = open(filename)
    hosts = json.load(file)

    host_protocols = dict()
    for host in hosts:
        ip = host['ip']
        protocol = host['protocol']
        if ip not in host_protocols:
            host_protocols[ip] = [protocol]
        else:
            if protocol not in host_protocols[ip]:
                host_protocols[ip].append(protocol)

    protocol_count = [len(v) for v in host_protocols.values()]

    max_n = max(protocol_count)

    plt.rc('font', size=15)

    plt.bar([str(i) for i in range(1, max_n + 1)], [sum(1 for j in protocol_count if j == i) for i in range(1, max_n + 1)],
        color=('lightcoral' if plot_type == 'honeypot' else 'royalblue'))
    plt.yscale('log')
    plt.gca().yaxis.set_major_formatter(mticker.ScalarFormatter())

    if plot_type == 'honeypot':
        plt.xlabel('Number of emulated industrial protocols')
        plt.ylabel('Number of honeypots')
    else:
        plt.xlabel('Number of hosted industrial protocols')
        plt.ylabel('Number of devices')
        
    plt.savefig(output_file, bbox_inches='tight')


if __name__ == '__main__':
    main()
