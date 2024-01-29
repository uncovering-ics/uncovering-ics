#!/usr/bin/env python3

import json
from sys import argv

from tabulate import tabulate

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    protocols = dict()
    
    for host in hosts:
        protocol = host['protocol']
        if protocol not in protocols:
            protocols[protocol] = list()
        protocols[protocol].append(host)

    protocols["Total"] = hosts

    rows = []

    honeypot_indications = ['classification_likely_honeypot', 'classification_honeypot']
    real_indications = ['classification_potentially_real']

    for protocol, hosts in protocols.items():
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

    headers = ["Protocol", "IPs (Honeypots)", "ASes (Honeypots)", "Countries (Honeypots)"]
    print(tabulate([headers] + rows, headers="firstrow"))
    print()
    print(tabulate([headers] + rows, headers="firstrow", tablefmt='latex'))
    
    


if __name__ == '__main__':
    main()
