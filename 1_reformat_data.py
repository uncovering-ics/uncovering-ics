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

        host_as = host.get('autonomous_system', {})
        asn = host_as.get('asn', None)
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

        s7 = []
        for s in host['services']:
            if s.get('service_name') != 'S7' or 's7' not in s:
                continue
            s7.append({
                'port': s['port'],
                'plant_id': s['s7'].get('plant_id'),
                'system': s['s7'].get('system'),
                'serial_number': s['s7'].get('serial_number'),
                'reserved_for_os': s['s7'].get('reserved_for_os'),
            })
        res['s7'] = s7

        atg = []
        for s in host['services']:
            if s.get('service_name') != 'ATG':
                continue
            atg.append({
                'port': s['port'],
                'banner_hex': s.get('banner_hex'),
            })
        res['atg'] = atg

        http = []
        for s in host['services']:
            if s.get('service_name') != 'HTTP':
                continue
            http.append(s.get('http', {}).get('response', {}) | {'port': s['port']})
        res['http'] = http

        banner_hashes = []
        for s in host['services']:
            for hash in s.get('banner_hashes', []):
                banner_hashes.append({
                    'service_name': s['service_name'],
                    'port': s['port'],
                    'hash': hash,
                })
        res['banner_hashes'] = banner_hashes


        host_results.append(res)
    
    print(json.dumps(host_results, indent=4))

if __name__ == '__main__':
    main()
