#!/usr/bin/env python3

import json
from sys import argv
from parameters import *
import maxminddb

def add_as_categories(host, ipinfo):
    ip = host['ip']
    asn = host['asn']

    ipinfo_data = ipinfo.get(ip)

    assert ipinfo_data is not None

    host['ipinfo'] = {
        'company': {
            'name': ipinfo_data['name'],
            'domain': ipinfo_data['domain'],
            'type': ipinfo_data['type'],
        },
        'as': {
            'asn': ipinfo_data['asn'],
            'name': ipinfo_data['as_name'],
            'domain': ipinfo_data['as_domain'],
            'type': ipinfo_data['as_type'],
        },
    }

# main logic

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    with maxminddb.open_database('./standard_company.mmdb') as ipinfo:
        for i in range(len(hosts)):
            host = hosts[i]
            add_as_categories(host, ipinfo)
    
    print(json.dumps(hosts, indent=4))

if __name__ == '__main__':
    main()
