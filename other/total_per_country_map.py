#!/usr/bin/env python3

import json
from sys import argv
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
import numpy as np
import geopandas as gpd
from pycountry import countries as country_data

def draw_classifications_per_country_map(countries, output_file, cmap):
    plt.figure()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[world['name'] != 'Antarctica'] # remove Antarctica

    fig, ax = plt.subplots(figsize=(15, 15))

    plt.rc('font', size=14)
    world.plot(ax=ax, edgecolor=u'grey', color='#999999')

    cm = plt.cm.ScalarMappable(cmap=cmap, 
        norm=mcolors.LogNorm(vmin=max(10, min(countries.values())), vmax=max(countries.values())))


    for country, num in countries.items():
        color = cm.to_rgba(num)
        world.loc[world['iso_a3'].eq(country_data.get(alpha_2=country).alpha_3)] \
            .plot(edgecolor=u'grey', color=color, ax=ax, aspect=1)

    # draw legend
    cb_ax = fig.add_axes([0.15, 0.355, 0.015, 0.15])  # [left, bottom, width, height]
    cm.set_array([])
    cb = plt.colorbar(cm, cax=cb_ax,
        format=mticker.ScalarFormatter())

    ax.axis('off')
    ax.margins(0)
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    cmap = argv[2]
    output_file = argv[3]

    countries = {}
    
    for host in hosts:
        if host['country_code'] not in countries:
            countries[host['country_code']] = set()
        countries[host['country_code']].add(host['ip'])

    draw_classifications_per_country_map({c: len(v) for c,v in countries.items()}, output_file, cmap)

if __name__ == '__main__':
    main()
