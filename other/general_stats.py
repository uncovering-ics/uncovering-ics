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

    for protocol, hosts in protocols.items():
        f = lambda field, classification: [h[field] for h in hosts if h['classification'] == classification]

        ips_real = f('ip', 'potentially_real')
        ips_honeypot_low = f('ip', 'honeypot_low_confidence')
        ips_honeypot_medium = f('ip', 'honeypot_medium_confidence')
        ips_honeypot_high = f('ip', 'honeypot_high_confidence')

        ases_real = f('asn', 'potentially_real')
        ases_honeypot_low = f('asn', 'honeypot_low_confidence')
        ases_honeypot_medium = f('asn', 'honeypot_medium_confidence')
        ases_honeypot_high = f('asn', 'honeypot_high_confidence')

        countries_real = f('country_code', 'potentially_real')
        countries_honeypot_low = f('country_code', 'honeypot_low_confidence')
        countries_honeypot_medium = f('country_code', 'honeypot_medium_confidence')
        countries_honeypot_high = f('country_code', 'honeypot_high_confidence')

        assert len(ips_real) + len(ips_honeypot_low) + len(ips_honeypot_medium) + len(ips_honeypot_high) == len(hosts)
        assert len(ases_real) + len(ases_honeypot_low) + len(ases_honeypot_medium) + len(ases_honeypot_high) == len(hosts)
        assert len(countries_real) + len(countries_honeypot_low) + len(countries_honeypot_medium) + len(ases_honeypot_high) == len(hosts)

        rows.append((len(hosts), 
            [
                protocol,
                len(set(ips_real)), len(set(ips_honeypot_low)), len(set(ips_honeypot_medium)), len(set(ips_honeypot_high)),
                len(set(ases_real)), len(set(ases_honeypot_low)), len(set(ases_honeypot_medium)), len(set(ases_honeypot_high)),
                len(set(countries_real)), len(set(countries_honeypot_low)), len(set(countries_honeypot_medium)), len(set(countries_honeypot_high)),
            ]))



    rows = [r[1] for r in sorted(rows, key=lambda r: r[0], reverse=True)]

    headers = ["Protocol",
               "Hosts: Real", "HP Low", "HP Medium", "HP High",
               "ASes: Real", "HP Low", "HP Medium", "HP High",
               "Countries: Real", "HP Low", "HP Medium", "HP High"
               ]
    print(tabulate([headers] + rows, headers="firstrow"))
    print()
    print(tabulate([headers] + rows, headers="firstrow", tablefmt='latex'))
    
    


if __name__ == '__main__':
    main()
