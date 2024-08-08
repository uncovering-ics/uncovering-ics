#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import AutoMinorLocator
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
import numpy as np
import geopandas as gpd
from pycountry import countries as country_data

classification_config = [
    ('potentially_real', 'Potentially real', 'royalblue'),
    ('honeypot_low_confidence', 'Low-confidence honeypots', 'lightcoral'),
    ('honeypot_medium_confidence', 'Medium-confidence honeypots', 'indianred'),
    ('honeypot_high_confidence', 'High-confidence honeypots', 'firebrick'),
]

all_classifications = [c[0] for c in classification_config]

def print_country(country_name, country_dict):
    all_sum = sum(country_dict.values())
    print(f"{country_name} - {all_sum} hosts")
    for cl in all_classifications:
        percentage = country_dict[cl] * 100 / all_sum
        print(f"    {cl.ljust(30)} {str(country_dict[cl]).rjust(5)}, {percentage:.1f}%")
    print()

def draw_classifications_per_country_map(countries, output_file, global_classifications):  
    plt.figure()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world['name'] != 'Antarctica'] # remove Antarctica

    fig, ax = plt.subplots(figsize=(15, 15))

    plt.rc('font', size=14)
    world.plot(ax=ax, edgecolor=u'grey', color='#999999')

    global_baseline_real = 1 - (global_classifications['honeypot_medium_confidence'] + global_classifications['honeypot_high_confidence']) / sum(global_classifications.values())

    # cm = plt.cm.ScalarMappable(cmap='RdYlBu', norm=plt.Normalize(0.3, 1))
    cm = plt.cm.ScalarMappable(cmap='RdYlBu', norm=mcolors.TwoSlopeNorm(global_baseline_real, 0.3, 1))

    for country, country_dict in countries.items():
        all_sum = sum(country_dict.values())

        honeypot_proportion = (country_dict['honeypot_medium_confidence'] + country_dict['honeypot_high_confidence']) / all_sum

        real_proportion = 1 - honeypot_proportion

        color = cm.to_rgba(real_proportion)

        world.loc[world['iso_a3'].eq(country_data.get(alpha_2=country).alpha_3)] \
            .plot(edgecolor=u'grey', color=color, ax=ax, aspect=1)

    # draw legend
    cb_ax = fig.add_axes([0.15, 0.355, 0.015, 0.1])  # [left, bottom, width, height]
    cm.set_array([])
    cb = plt.colorbar(cm, cax=cb_ax)
    cb.set_ticks([0.3, 0.55, global_baseline_real, 0.95, 1.0])
    cb.set_ticklabels([
        '≥70% honeypots',
        '45% honeypots',
        'Global baseline',
        '5% honeypots',
        '0% honeypots'
    ])

    ax.axis('off')
    ax.margins(0)
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)


def draw_classifications_top(countries, output_file, top_countries):
    width = 0.35
    plt.figure()
    ind = np.arange(len(top_countries))
    plt.rc('font', size=15)
    # plt.yscale("log")]
    bottom = np.zeros(len(top_countries))
    for cl, _, color in classification_config:
        hosts = [countries[c][cl] for c in top_countries]
        plt.bar(ind, hosts, width, bottom=bottom, color=color)
        bottom += hosts
    plt.ylabel('Number of hosts')
    plt.xticks(ind, top_countries)
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())

    plt.legend(labels=[c[1] for c in classification_config], loc='upper right')

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
        clas = host['classification']
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

    draw_classifications_per_country_map(countries, output_file_map, global_classifications)

    draw_classifications_top(countries, output_file_top, top_countries[:15])

if __name__ == '__main__':
    main()
