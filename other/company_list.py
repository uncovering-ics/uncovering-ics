#!/usr/bin/env python3

import json
from sys import argv
import pandas as pd

def main():
    filename = argv[1]
    file = open(filename)
    hosts = json.load(file)

    data = [
        {
            'country': h['country_code'],
            'company_type': h['ipinfo']['company']['type'],
            'company_name': h['ipinfo']['company']['name'],
            'company_domain': h['ipinfo']['company']['domain'],
            'asn': f"AS{h['asn']}",
            'as_type': h['ipinfo']['as']['type'],
            'as_name_ipinfo': h['ipinfo']['as']['name'],
            'as_name_censys': h['as_name'],
            'as_domain': h['ipinfo']['as']['domain'],
        }
        for h in hosts
    ]

    frame = pd.DataFrame.from_records(data)
    frame_with_count = frame \
        .value_counts().reset_index()
    frame_with_count.columns = frame.columns.values.tolist() + ['count']
    frame_sorted = frame_with_count \
        .sort_values(['country', 'count'], ascending=[True, False])

    print(frame_sorted.to_csv(index=False))

if __name__ == '__main__':
    main()
