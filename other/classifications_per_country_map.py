#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import AutoMinorLocator
import matplotlib.cm as cmx
import numpy as np
import geopandas as gpd
from pycountry import countries as country_data

all_classifications = [
    'classification_potentially_real',
    'classification_likely_honeypot',
    'classification_honeypot',
]

def print_country(country_name, country_dict):
    all_sum = sum(country_dict.values())
    print(f"{country_name} - {all_sum} hosts")
    for cl in all_classifications:
        percentage = country_dict[cl] * 100 / all_sum
        print(f"    {cl.replace('classification_', '').ljust(16)} {str(country_dict[cl]).rjust(5)}, {percentage:.1f}%")
    print()

def draw_classifications_per_country_map(countries, output_file):
    plt.figure()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world['name'] != 'Antarctica'] # remove Antarctica

    fig, ax = plt.subplots(figsize=(15, 15))

    plt.rc('font', size=14)
    world.plot(ax=ax, edgecolor=u'grey', color='#999999')

    cm = plt.cm.ScalarMappable(cmap='RdYlBu', norm=plt.Normalize(0.3, 1))

    for country, country_dict in countries.items():
        all_sum = sum(country_dict.values())

        real_proportion = country_dict['classification_potentially_real'] / all_sum

        color = cm.to_rgba(real_proportion)

        world.loc[world['iso_a3'].eq(country_data.get(alpha_2=country).alpha_3)] \
            .plot(edgecolor=u'grey', color=color, ax=ax, aspect=1)

    # draw legend
    cb_ax = fig.add_axes([0.15, 0.355, 0.015, 0.1])  # [left, bottom, width, height]
    cm.set_array([])
    cb = plt.colorbar(cm, cax=cb_ax)
    cb.set_ticks([0.3, 0.5, 0.75, 1.0])
    cb.set_ticklabels([
        '≥70% honeypots',
        '50% honeypots',
        '25% honeypots',
        '0% honeypots'
    ])

    ax.axis('off')
    ax.margins(0)
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)


def draw_classifications_top(countries, output_file, top_countries):
    real = [countries[c]['classification_potentially_real'] for c in top_countries]
    honeypot = [countries[c]['classification_likely_honeypot'] + countries[c]['classification_honeypot'] for c in top_countries]

    width = 0.35
    plt.figure()
    ind = np.arange(len(top_countries))
    plt.rc('font', size=13)
    # plt.yscale("log")
    plt.bar(ind, real, width, color='royalblue')
    plt.bar(ind, honeypot, width, bottom=real, color='lightcoral')
    plt.ylabel('Number of hosts')
    plt.xticks(ind, top_countries)
    # plt.xticks(ind, top_countries)
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())

    plt.legend(labels=['Classified as real', 'Suspected honeypots'], loc='upper right')

    plt.savefig(output_file, bbox_inches='tight')

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    output_file_map = argv[2]
    output_file_top = argv[3]

    countries = {}
    global_classifications = {c: 0 for c in all_classifications}
    
    for host in hosts:
        clas = next(filter(lambda i: i in all_classifications, host['indications']))
        if host['country_code'] in countries:
            country_dict = countries[host['country_code']]
        else:
            country_dict = countries[host['country_code']] = {c: 0 for c in all_classifications}
        country_dict[clas] += 1
        global_classifications[clas] += 1

    print_country("Global", global_classifications)

    top_countries = sorted(countries.keys(), key=lambda x: -sum(countries[x].values()))
    for country in top_countries:
        print_country(country, countries[country])

    draw_classifications_per_country_map(countries, output_file_map)

    draw_classifications_top(countries, output_file_top, top_countries[:15])

if __name__ == '__main__':
    main()
