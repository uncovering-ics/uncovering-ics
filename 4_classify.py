#!/usr/bin/env python3

import json
from sys import argv
from parameters import *

classification_unknown = 'potentially_real'
classification_honeypot_low = 'honeypot_low_confidence'
classification_honeypot_medium = 'honeypot_medium_confidence'
classification_honeypot_high = 'honeypot_high_confidence'

def classify(indications):

    # we have observed honeypot signatures
    signature_criterium = any(x in indications for x in ['honeypot_defaults_conpot', 'honeypot_defaults_snap7', 'gaspot_newlines', 'gaspot_date'])
    if signature_criterium:
        return classification_honeypot_high

    # it's at a datacenter
    hosting_criterium = any(x in indications for x in ['as_hosting', 'company_hosting'])
    if hosting_criterium:
        return classification_honeypot_medium
    
    # it has too many open ports (high)
    port_criterium_high = 'many_open_ports_high' in indications
    if port_criterium_high:
        return classification_honeypot_medium

    # it's at a university
    education_criterium = any(x in indications for x in ['as_education', 'company_education'])

    # it has too many open ports
    port_criterium = 'many_open_ports' in indications

    if education_criterium and port_criterium:
        return classification_honeypot_medium

    if education_criterium or port_criterium:
        return classification_honeypot_low

    return classification_unknown

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    for i in range(len(hosts)):
        host = hosts[i]

        indications = set(host['indications'])

        label = classify(indications)
        host['classification'] = label
    
    print(json.dumps(hosts, indent=4))

if __name__ == '__main__':
    main()
