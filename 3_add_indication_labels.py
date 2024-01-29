#!/usr/bin/env python3

import json
from sys import argv
from parameters import *

# indication functions

def many_open_ports(host):
    open_port_count = host['open_port_count']
    if open_port_count > honeypot_open_port_threshold:
        return ['many_open_ports']
    return []

def network_indication(host):
    as_type = host['ipinfo']['as']['type']
    company_type = host['ipinfo']['company']['type']
    indications = []
    if as_type == 'hosting':
        indications.append('as_hosting')
    if as_type == 'education':
        indications.append('as_education')
    if company_type == 'hosting':
        indications.append('company_hosting')
    if company_type == 'education':
        indications.append('company_education')
    return indications
    
def honeypot_default(host):
    if not host.get('s7', None):
        return []
    for honeypot_name, defaults in honeypot_defaults.items():
        for d_name, d_value in defaults.items():
            if d_name in host['s7'] and host['s7'][d_name] == d_value:
                return [f'honeypot_defaults_{honeypot_name}']
    return []
    

indication_functions = [
    many_open_ports,
    network_indication,
    honeypot_default,
]

# main logic

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    for i in range(len(hosts)):
        host = hosts[i]

        indications = []
        for f in indication_functions:
            new_indications = f(host)
            indications += new_indications

        # build result
        host['indications'] = indications
    
    print(json.dumps(hosts, indent=4))

if __name__ == '__main__':
    main()
