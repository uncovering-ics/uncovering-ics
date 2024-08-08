#!/usr/bin/env python3

import json
from sys import argv
from parameters import *
import re

s7_honeypot_defaults = {
    'conpot': { # https://github.com/mushorg/conpot/blob/f0e6925fb9632172922abe41b293d7ee438fa60b/conpot/templates/default/template.xml
        'plant_id': 'Mouser Factory',
        'serial_number': '88111222',
    },
    'snap7': { # https://github.com/SCADACS/snap7/blob/f6ff90317ca5d54250f4dcd29209689a74e26d82/examples/plain-c/server.c
        'system': 'SNAP7-SERVER',
        'serial_number': 'S C-C2UR28922012',
        'reserved_for_os': 'MMC 267FF11F',
    },
}

# indication functions

def many_open_ports(host):
    open_port_count = host['open_port_count']
    if open_port_count > honeypot_open_port_threshold:
        return ['many_open_ports']
    return []

def many_open_ports_high(host):
    open_port_count = host['open_port_count']
    if open_port_count > honeypot_open_port_threshold_high:
        return ['many_open_ports_high']
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

def s7_honeypot_default(host):
    for s7 in host['s7']:
        for honeypot_name, defaults in s7_honeypot_defaults.items():
            for d_name, d_value in defaults.items():
                if d_name in s7 and s7[d_name] == d_value:
                    return [f'honeypot_defaults_{honeypot_name}']
    return []

# https://censys.com/red-herrings-and-honeypots/
def gaspot_newlines(host):
    for atg in host['atg']:
        if atg['banner_hex'] is None:
            continue
        if '0a0a0a0a' in atg['banner_hex']: # \n\n\n\n instead of \r\n\r\n
            return [f'gaspot_newlines']
    return []

# https://censys.com/red-herrings-and-honeypots/
def gaspot_date(host):
    for atg in host['atg']:
        if atg['banner_hex'] is None:
            continue
        banner = bytes.fromhex(atg['banner_hex'])
        # incorrect date format
        if re.search(b'\\n(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/[0-9]{4} ([01][0-9]|2[0-3]):([0-5][0-9])', banner):
            return [f'gaspot_date']
    return []


indication_functions = [
    many_open_ports,
    many_open_ports_high,
    network_indication,
    s7_honeypot_default,
    gaspot_newlines,
    gaspot_date,

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
