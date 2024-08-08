#!/usr/bin/env python3
import matplotlib.pyplot as plt
import json
from sys import argv

input_filename = argv[1]
output_filename = argv[2]

file = open(input_filename)
hosts = json.load(file)

ases = dict()
as_names = dict()

for host in hosts:
    ip = host['ip']
    asn = host['asn']
    as_name = host['as_name']
    if asn not in ases:
        ases[asn] = set()
        as_names[asn] = as_name
    ases[asn].add(ip)


ases_n = {f'AS{asn} {as_names[asn] if len(as_names[asn]) < 13 else as_names[asn][:12]+"..."}': len(h) for asn, h in ases.items()}

as_names = list(sorted(ases_n.keys(), key=lambda asn: ases_n[asn], reverse=True))

as_names_top = as_names[:5] + ['others']
ases_n['others'] = sum(ases_n[as_name] for as_name in as_names[5:])

wdges, labels, autopct = plt.pie([ases_n[as_name] for as_name in as_names_top], labels=as_names_top, autopct='%1.1f%%', shadow=True,
    startangle=(0 if ases_n[as_names_top[0]] / sum(ases_n[as_name] for as_name in as_names_top) > 0.25 else 90))
plt.setp(labels, fontsize=14)
for l in labels[:-1]:
    l.set_ha('right')
plt.savefig(output_filename, bbox_inches='tight', pad_inches=0)
