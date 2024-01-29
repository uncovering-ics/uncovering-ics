#!/usr/bin/env python3

import json
from sys import argv
from parameters import *

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    host_results = []

    seen = set()

    for i in range(len(hosts)):
        host = hosts[i]

        # extract censys data
        ip = host['ip']

        open_port_count = int(host['service_count'])
        country_code = host['location']['country_code']

        # skip duplicates
        if ip in seen:
            continue
        seen.add(ip)

        host_as = host['autonomous_system']
        asn = host_as['asn']
        as_name = host_as.get('name', '')

        reverse_dns = host.get('dns', {}).get('reverse_dns', {}).get('names', [None])[0]

        # build result
        res = {
            'ip': ip,
            'reverse_dns': reverse_dns,
            'asn': asn,
            'country_code': country_code,
            'as_name': as_name,
            'open_port_count': open_port_count
        }

        if 'services' in host:
            res['s7'] = host['services'][0]['s7']

        host_results.append(res)
    
    print(json.dumps(host_results, indent=4))

if __name__ == '__main__':
    main()
