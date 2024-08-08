#!/usr/bin/env python3
import matplotlib.pyplot as plt
import json
from sys import argv
from pycountry import countries as country_data

input_filename = argv[1]
output_filename = argv[2]

file = open(input_filename)
hosts = json.load(file)

countries = dict()

for host in hosts:
    ip = host['ip']
    country = host['country_code']
    if country not in countries:
        countries[country] = set()
    countries[country].add(ip)


countries_n = {country_data.get(alpha_2=c).common_name: len(h) for c, h in countries.items()}

country_names = list(sorted(countries_n.keys(), key=lambda c: countries_n[c], reverse=True))

country_names_top = country_names[:9] + ['others']
countries_n['others'] = sum(countries_n[c] for c in country_names[9:])

plt.rc('font', size=13)
plt.pie([countries_n[c] for c in country_names_top], labels=country_names_top, autopct='%1.1f%%', shadow=True,
    startangle=(0 if countries_n[country_names_top[0]] / sum(countries_n[c] for c in country_names_top) > 0.25 else 90))
plt.savefig(output_filename, bbox_inches='tight', pad_inches=0)
