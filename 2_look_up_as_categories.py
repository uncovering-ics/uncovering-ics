#!/usr/bin/env python3

import json
from sys import argv
from parameters import *
import csv
import maxminddb

asdb_categories = {}

def add_as_categories(host, ipinfo):
    ip = host['ip']
    asn = host['asn']
    host['asdb_categories'] = asdb_categories.get(asn, [])

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

def load_asdb():
    with open('2023-05_categorized_ases.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_skipped = False
        for row in reader:
            if not first_skipped or len(row) == 0:
                first_skipped = True
                continue
            assert row[0][:2] == 'AS'
            asn = int(row[0][2:])
            categories = [[row[i], row[i+1] if len(row[i+1]) > 0 else None] for i in range(1, len(row), 2)]
            asdb_categories[asn] = categories

# main logic

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    load_asdb()

    with maxminddb.open_database('./artifacts_v1_standard_company.mmdb') as ipinfo:
        for i in range(len(hosts)):
            host = hosts[i]
            add_as_categories(host, ipinfo)
    
    print(json.dumps(hosts, indent=4))

if __name__ == '__main__':
    main()
