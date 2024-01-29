#!/usr/bin/env python3
import matplotlib.pyplot as plt
import json
from sys import argv

input_filename = argv[1]
output_filename = argv[2]

file = open(input_filename)
hosts = json.load(file)

company_types = ['isp', 'business', 'hosting', 'education']
host_types = {a: set() for a in company_types}

for host in hosts:
    ip = host['ip']
    company_type = host['ipinfo']['company']['type']
    host_types[company_type].add(ip)

present_company_types = [c for c in company_types if len(host_types[c]) > 0]

plt.rc('font', size=14)
plt.pie([len(host_types[c]) for c in present_company_types], labels=present_company_types,
    autopct='%1.1f%%', shadow=True)
plt.savefig(output_filename, bbox_inches='tight')
