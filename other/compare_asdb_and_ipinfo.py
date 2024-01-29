#!/usr/bin/env python3

import csv

asdb_hosting_ases = set()
asdb_education_ases = set()

ipinfo_hosting_ases = set()
ipinfo_education_ases = set()
ipinfo_all = set()

def load_asdb():
    with open('../2023-05_categorized_ases.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_skipped = False
        for row in reader:
            if not first_skipped or len(row) == 0:
                first_skipped = True
                continue
            assert row[0][:2] == 'AS'
            asn = row[0]
            categories = [[row[i], row[i+1] if len(row[i+1]) > 0 else None] for i in range(1, len(row), 2)]
            for c1, c2 in categories:
                if c1 == 'Education and Research':
                    asdb_education_ases.add(asn)
                if c1 == 'Computer and Information Technology' and c2 == 'Hosting and Cloud Provider':
                    asdb_hosting_ases.add(asn)

def load_ipinfo():
    with open('../as_ipinfo.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_skipped = False
        for row in reader:
            if not first_skipped or len(row) == 0:
                first_skipped = True
                continue
            assert row[0][:2] == 'AS'
            asn = row[0]
            ipinfo_type = row[1]
            ipinfo_all.add(asn)
            if ipinfo_type == 'hosting':
                ipinfo_hosting_ases.add(asn)
            if ipinfo_type == 'education':
                ipinfo_education_ases.add(asn)

def main():
    load_ipinfo()
    load_asdb()

    print("Total ASdb education:  ", len(asdb_education_ases.intersection(ipinfo_all)))
    print("Total IPinfo education:", len(ipinfo_education_ases))
    print("Education intersection:", len(asdb_education_ases.intersection(ipinfo_education_ases)))
    print("Total ASdb hosting:    ", len(asdb_hosting_ases.intersection(ipinfo_all)))
    print("Total IPinfo hosting:  ", len(ipinfo_hosting_ases))
    print("Hosting intersection:  ", len(asdb_hosting_ases.intersection(ipinfo_hosting_ases)))

    print("\nEducation in ASdb but not IPinfo:")
    for asn in (asdb_education_ases.intersection(ipinfo_all) - ipinfo_education_ases):
        print(asn)
    print("\nEducation in IPinfo but not ASdb:")
    for asn in (ipinfo_education_ases - asdb_education_ases.intersection(ipinfo_all)):
        print(asn)
    print("\nHosting in ASdb but not IPinfo:")
    for asn in (asdb_hosting_ases.intersection(ipinfo_all) - ipinfo_hosting_ases):
        print(asn)
    print("\nHosting in IPinfo but not ASdb:")
    for asn in (ipinfo_hosting_ases - asdb_hosting_ases.intersection(ipinfo_all)):
        print(asn)

if __name__ == '__main__':
    main()
