#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
from sys import argv
import matplotlib.ticker as mticker
from matplotlib import rcParams



# colourblind-friendly colours: https://gist.github.com/thriveth/8560036
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628']
labels = ['All types', 'hosting', 'education', 'isp', 'business']
linestyles = ['solid', 'dashed', 'dotted', 'dashdot', (0, (5, 1))]

input_filename = argv[1]
output_filename = argv[2]

file = open(input_filename)
hosts = json.load(file)

as_hosts = {}
as_types = {p: set() for p in labels[1:]}

for host in hosts:
    ip = host['ip']
    asn = host['ipinfo']['as']['asn']
    as_type = host['ipinfo']['as']['type']
    if asn not in as_hosts:
        as_hosts[asn] = set()
        as_types[as_type].add(asn)
    else:
        assert asn in as_types[as_type], f"{asn} expected to be {as_type}"
    as_hosts[asn].add(ip)

def calc_cdf(as_set):
    data = list(len(as_hosts[asn]) for asn in as_set)
    x = np.sort([0]+data)
    y = np.arange(len(data)+1) / float(len(data))
    return x, y

def apply_matplotlib_settings():
    plt.rc('font', size=14)
    plt.xlabel('Max. suspected honeypots within one AS', fontsize=16)
    plt.ylabel('Proportion of observed ASes', fontsize=16)
    plt.grid()
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter())
    plt.gca().yaxis.set_major_formatter(mticker.ScalarFormatter())
    plt.legend(loc="lower right", ncol=1)

plt.figure()

for color, linestyle, as_type, asns in \
        zip(CB_color_cycle, linestyles, labels, [as_hosts.keys()] + [as_types[t] for t in labels[1:]]):
    prot_x, prot_y = calc_cdf(asns)
    plt.plot(prot_x, prot_y, color=color, label=as_type, linestyle=linestyle)

apply_matplotlib_settings()
plt.savefig(output_filename, bbox_inches='tight')
