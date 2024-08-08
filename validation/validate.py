#!/usr/bin/env python3

import sys
import json
import multiprocessing

import validate_modbus
import validate_s7

validation_results = {
    None: 'cannot_connect',
    True: 'honeypot',
    False: 'no_match'
}

def process_host(host):
    ip = host['ip']
    protocol = host['protocol']

    validator = None
    if host['protocol'] == 'MODBUS':
        validator = validate_modbus
    elif host['protocol'] == 'S7':
        validator = validate_s7

    res, msg = validator.validate(ip)

    host['validation'] = validation_results[res]
    host['validation_msg'] = msg

    with curr.get_lock():
        curr.value += 1
        print(f"[{curr.value}/{total}] ({host['protocol']}) Validated {ip}: {host['validation']}", file=sys.stderr)

    return host

def worker_setup(c, t):
    global curr, total
    curr, total = c, t
    

def main():
    filename = sys.argv[1]
    file = open(filename)
    hosts = json.load(file)
    total = len(hosts)
    print(f'Loaded {total} hosts', file=sys.stderr)

    curr = multiprocessing.Value('i', 0)
    pool = multiprocessing.Pool(initializer=worker_setup, initargs=[curr, total], processes=64) # connect to 64 hosts at a time
    results = pool.map(process_host, hosts)        
    
    print(json.dumps(results, indent=4))


if __name__ == '__main__':
    main()
