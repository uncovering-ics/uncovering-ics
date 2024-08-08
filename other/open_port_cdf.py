#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
from sys import argv
import matplotlib.ticker as mticker
from matplotlib import rcParams

input_filename = argv[1]
output_network_filename = argv[2]
output_honeypot_filename = argv[3]

file = open(input_filename)
hosts = json.load(file)

all_open_ports_per_host = dict()
# education_hosts = set()
hosting_hosts = set()
honeypot_hosts = set()

honeypot_classifications = ['honeypot_medium_confidence', 'honeypot_high_confidence']

for host in hosts:
    ip = host['ip']
    open_port_count = host['open_port_count']
    all_open_ports_per_host[ip] = max(all_open_ports_per_host.get(ip, 0), open_port_count)
    # if any(ind in ['company_education', 'as_education'] for ind in host['indications']):
    #     education_hosts.add(ip)
    if any(ind in ['company_hosting', 'as_hosting'] for ind in host['indications']):
        hosting_hosts.add(ip)
    if host['classification'] in honeypot_classifications:
        honeypot_hosts.add(ip)

def calc_cdf(host_set):
    data = list(all_open_ports_per_host[ip] for ip in host_set)
    x = np.sort([0]+data)
    y = np.arange(len(data)+1) / float(len(data))
    return x, y

all_x, all_y = calc_cdf(all_open_ports_per_host.keys())
honeypot_x, honeypot_y = calc_cdf(honeypot_hosts)
# education_x, education_y = calc_cdf(education_hosts)
hosting_x, hosting_y = calc_cdf(hosting_hosts)

def apply_matplotlib_settings():
    plt.rc('font', size=16)
    plt.xlabel('Maximum number of open ports', fontsize=16)
    plt.ylabel('Proportion of observed hosts', fontsize=16)
    plt.grid()
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter())
    plt.legend(loc="lower right")

plt.figure()
plt.plot(all_x, all_y, label="All hosts", linestyle='solid')
plt.plot(hosting_x, hosting_y, color="indianred", label="Hosts on datacenter networks", linestyle='dashed')
# plt.plot(education_x, education_y, color="darkviolet", label="Hosts on academic networks", linestyle='dotted')
apply_matplotlib_settings()
plt.savefig(output_network_filename, bbox_inches='tight')

plt.figure()
plt.plot(all_x, all_y, label="All hosts", linestyle='solid')
plt.plot(honeypot_x, honeypot_y, color="firebrick", label="Suspected honeypots", linestyle='dashed')
apply_matplotlib_settings()
plt.savefig(output_honeypot_filename, bbox_inches='tight')

print('P(num_open_ports < 10) =', (all_x < 10).mean())
print('P(num_open_ports < 30) =', (all_x < 30).mean())
print('P(num_open_ports < 100) =', (all_x < 100).mean())
# print('P(num_open_ports < 10 | academic network) =', (education_x < 10).mean())
print('P(num_open_ports > 10 | datacenter network) =', (hosting_x > 10).mean())
print('P(num_open_ports > 30 | datacenter network) =', (hosting_x > 30).mean())
print('P(num_open_ports > 100 | datacenter network) =', (hosting_x > 100).mean())
print('P(num_open_ports > 10 | classified as honeypot) =', (honeypot_x > 10).mean())
print('P(num_open_ports > 30 | classified as honeypot) =', (honeypot_x > 30).mean())
print('P(num_open_ports > 100 | classified as honeypot) =', (honeypot_x > 100).mean())
print('P(num_open_ports > 1000 | classified as honeypot) =', (honeypot_x > 1000).mean())
