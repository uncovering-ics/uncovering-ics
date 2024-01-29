#!/usr/bin/env python3

import json
from sys import argv

from tabulate import tabulate

TARGET_CATEGORIES = [
    'Agriculture, Mining, and Refineries (Farming, Greenhouses, Mining, Forestry, and Animal Farming)',
    'Utilities (Excluding Internet Service)',
    'Government and Public Administration',
    'Manufacturing',
]

honeypot_indications = ['classification_likely_honeypot', 'classification_honeypot']
real_indications = ['classification_potentially_real']

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    categories = {c: [] for c in TARGET_CATEGORIES}
    
    for host in hosts:
        # exclude if hosting/education
        if any(x in host['indications'] for x in ['as_hosting', 'as_education', 'company_hosting', 'company_education']):
            continue
        for c in set(c[0] for c in host['asdb_categories'] if c[0] in categories):
            categories[c].append(host)

    rows = []

    for protocol, hosts in categories.items():
        real_ips = [h['ip'] for h in hosts \
            if any(ind in real_indications for ind in h['indications'])]

        honeypot_ips = [h['ip'] for h in hosts \
            if any(ind in honeypot_indications for ind in h['indications'])]

        real_ases = [h['asn'] for h in hosts \
            if any(ind in real_indications for ind in h['indications'])]

        honeypot_ases = [h['asn'] for h in hosts \
            if any(ind in honeypot_indications for ind in h['indications'])]

        real_countries = [h['country_code'] for h in hosts \
            if any(ind in real_indications for ind in h['indications'])]

        honeypot_countries = [h['country_code'] for h in hosts \
            if any(ind in honeypot_indications for ind in h['indications'])]

        assert len(real_ips) + len(honeypot_ips) == len(hosts)
        assert len(real_ases) + len(honeypot_ases) == len(hosts)
        assert len(real_countries) + len(honeypot_countries) == len(hosts)

        rows.append((len(hosts), 
            [
                protocol, 
                f'{len(set(real_ips)):,} ({len(set(honeypot_ips)):,})',
                f'{len(set(real_ases)):,} ({len(set(honeypot_ases)):,})',
                f'{len(set(real_countries)):,} ({len(set(honeypot_countries)):,})'
            ]))



    rows = [r[1] for r in sorted(rows, key=lambda r: r[0], reverse=True)]

    headers = ["ASdb category", "IPs (Honeypots)", "ASes (Honeypots)", "Countries (Honeypots)"]
    print(tabulate([headers] + rows, headers="firstrow"))
    print()
    print(tabulate([headers] + rows, headers="firstrow", tablefmt='latex'))

    for category, hosts in categories.items():
        print()
        print(f"{category}: {len(set(h['ip'] for h in hosts))}")
        # print(' '*4 + f"split per country:")
        countries = dict()
        for h in hosts:
            country = h['country_code']
            if country not in countries: countries[country] = []
            countries[country].append(h)
        for country, hosts in countries.items():
            print(' '*4 + f"{country}: {len(set(h['ip'] for h in hosts))}")
            # print(' '*8 + f"split per protocol:")
            protocols = dict()
            for h in hosts:
                protocol = h['protocol']
                if protocol not in protocols: protocols[protocol] = []
                protocols[protocol].append(h)
            for protocol, hosts in protocols.items():
                print(' '*8 + f"{protocol}: {len(set(h['ip'] for h in hosts))}")
                honeypots = [h for h in hosts if any(ind in honeypot_indications for ind in h['indications'])]
                real = [h for h in hosts if any(ind in real_indications for ind in h['indications'])]
                # print(' '*16 + "split per classification label:")
                for lbl, hosts in [("classified as honeypot", honeypots), ("classified as real", real)]:
                    print(' '*12 + f"{lbl}: {len(set(h['ip'] for h in hosts))}")
                    owners = dict()
                    for h in hosts:
                        owner = f"AS{h['asn']}, {h['as_name']}, company: {h['ipinfo']['company']['name'] if h['ipinfo']['company'] else 'unknown'}"
                        if owner not in owners: owners[owner] = []
                        owners[owner].append(h)
                    for owner, hosts in owners.items():
                        print(' '*16 + f"{owner}: {len(set(h['ip'] for h in hosts))}")

    
    


if __name__ == '__main__':
    main()
