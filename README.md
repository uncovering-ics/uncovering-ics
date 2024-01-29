## All that Glitters is not Gold: Uncovering Exposed Industrial Control Systems and Honeypots in the Wild

This is code related to the paper "All that Glitters is not Gold: Uncovering Exposed Industrial Control Systems and Honeypots in the Wild".

## Reproduction

The steps below can be used for reproduction of the research.

### Initial setup

Mark all scripts as executable: `chmod +x *.py *.sh other/*.py`

Download the [ASdb](https://asdb.stanford.edu/) dataset and save it as `2023-05_categorized_ases.csv` in this directory.

Download the [IPinfo IP to company database](https://ipinfo.io/products/ip-company-database) and save it as `artifacts_v1_standard_company.mmdb` in this directory.

Set up the [Censys CLI](https://censys-python.readthedocs.io/en/stable/usage-cli.html) on your machine.

### Data retrieval 

Download data from Censys for all countries and all protocols:

```
./download_all.sh
```

The downloaded files are stored under `data/<current date>`.

### Data processing

Process the files and generate statistics:

```
./run_all.sh <current date>
```

For example: `./run_all.sh 2023-12-06`

### Analysis

Statistics are stored under `data/<current date>/aggregated`.
