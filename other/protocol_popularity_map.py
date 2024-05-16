#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import geopandas as gpd
from pycountry import countries as country_data

# colourblind-friendly colours: https://gist.github.com/thriveth/8560036
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#e41a1c', '#36454f']
color_other = '#dede00'
common_protocols = ["MODBUS", "IEC60870_5_104", "FOX", "S7", "WDBRPC", "BACNET", "ATG", "EIP"] # top 8 with most devices
cm = dict(zip(common_protocols, CB_color_cycle))

def print_country(country_name, country_dict, all_protocols):
    all_sum = sum(country_dict.values())
    print(f"{country_name} - {all_sum} hosts")
    for protocol in sorted(all_protocols, key=lambda x: -country_dict.get(x, 0)):
        n = country_dict.get(protocol, 0)
        percentage = n * 100 / all_sum
        print(f"    {protocol.ljust(15)} {str(n).rjust(5)}, {percentage:.1f}%")
    print()

def draw_map(countries, output_file):
    plt.figure()
    color_no_data = '#999999'

    used_protocols = set()
    other_used = False

    plt.rc('font', size=14)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world['name'] != 'Antarctica'] # remove Antarctica

    ax = world.plot(figsize=(15,15), edgecolor=u'grey', color=color_no_data)

    for country, country_dict in countries.items():
        top_protocol = sorted(country_dict.keys(), key=lambda x: -country_dict[x])[0]
        if top_protocol in cm:
            color = cm[top_protocol]
            used_protocols.add(top_protocol)
        else:
            color = color_other
            other_used = True

        world.loc[world['iso_a3'].eq(country_data.get(alpha_2=country).alpha_3)] \
            .plot(edgecolor=u'grey', color=color, ax=ax, aspect=1)

    ax.legend(handles=[mpatches.Patch(color=c, label=l) for l, c in [(p, cm[p]) for p in common_protocols if p in used_protocols] + \
                      ([('Other', color_other)] if other_used else []) + [('No data', color_no_data)]],
               loc='lower left')

    ax.axis('off')
    ax.margins(0)
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)

def draw_top_proportions(countries, top_countries, output_file):
    plt.figure()
    plt.rc('font', size=11)
    plt.ylabel('Distribution of protocols')
    # plt.ylabel('Country')

    offsets = np.zeros(len(top_countries))
    countries_sum = {c: sum(countries[c].values()) for c in top_countries}

    common_protocols_7 = common_protocols[:7]
    for protocol in common_protocols_7:
        y = np.array([countries[c].get(protocol, 0) / countries_sum[c] for c in top_countries])
        plt.bar(top_countries, y, bottom=offsets, color=cm[protocol])
        offsets += y
    
    plt.bar(top_countries, np.ones(len(top_countries)) - offsets, bottom=offsets, color=color_other)

    plt.legend(labels=common_protocols_7 + ['Other'], bbox_to_anchor=(1.02, -0.063), ncol=4)

    plt.savefig(output_file, bbox_inches='tight')

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    output_file = argv[2]
    output_file_top = argv[3]

    countries = {}
    global_protocols = {}
    
    for host in hosts:
        protocol = host['protocol']
        country = host['country_code']
        if protocol not in global_protocols:
            global_protocols[protocol] = 0
        global_protocols[protocol] += 1

        if country not in countries:
            countries[country] = {}
        if protocol not in countries[country]:
            countries[country][protocol] = 0
        countries[country][protocol] += 1

    all_protocols = sorted(global_protocols.keys())

    print_country("Global", global_protocols, all_protocols)

    sorted_countries = sorted(countries.keys(), key=lambda x: -sum(countries[x].values()))

    for country in sorted_countries:
        print_country(country, countries[country], all_protocols)

    draw_map(countries, output_file)
    draw_top_proportions(countries | {"Global": global_protocols}, ["Global"] + sorted_countries[:10], output_file_top)

if __name__ == '__main__':
    main()
