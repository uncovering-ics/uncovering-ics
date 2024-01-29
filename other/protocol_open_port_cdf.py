#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
from sys import argv
import matplotlib.ticker as mticker
from matplotlib import rcParams

from protocol_popularity_map import cm, common_protocols

input_filename = argv[1]
output_filename = argv[2]
linestyle = argv[3]

file = open(input_filename)
hosts = json.load(file)

all_open_ports_per_host = dict()
protocol_hosts = {p: set() for p in common_protocols}

for host in hosts:
    ip = host['ip']
    protocol = host['protocol']
    open_port_count = host['open_port_count']
    all_open_ports_per_host[ip] = max(all_open_ports_per_host.get(ip, 0), open_port_count)
    if protocol in protocol_hosts:
        protocol_hosts[protocol].add(ip)

def calc_cdf(host_set):
    data = list(all_open_ports_per_host[ip] for ip in host_set)
    x = np.sort(data)
    y = np.arange(len(data)) / float(len(data))
    return x, y

def apply_matplotlib_settings():
    plt.rc('font', size=9)
    plt.xlabel('Maximum number of open ports')
    plt.ylabel('Proportion of observed hosts')
    plt.grid()
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter())
    plt.legend(loc="lower right", ncol=1)

plt.figure()

all_x, all_y = calc_cdf(all_open_ports_per_host.keys())
plt.plot(all_x, all_y, label="All protocols", linestyle='dotted')

for protocol in common_protocols:
    prot_x, prot_y = calc_cdf(protocol_hosts[protocol])
    plt.plot(prot_x, prot_y, color=cm[protocol], label=protocol, linestyle=linestyle)

apply_matplotlib_settings()
plt.savefig(output_filename, bbox_inches='tight')
