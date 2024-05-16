#!/bin/sh
set -eu

target_dir="$1"
country="$2"
protocol="$3"
curr_date="$4"
base_path="${target_dir}/${country}_${protocol}_${curr_date}"

./1_reformat_data.py "${base_path}_censys.json" > "${base_path}_intermediate_1.json"
./2_look_up_as_categories.py "${base_path}_intermediate_1.json" > "${base_path}_intermediate_2.json"
./3_add_indication_labels.py "${base_path}_intermediate_2.json" > "${base_path}_intermediate_3.json"
./4_classify.py "${base_path}_intermediate_3.json" > "${base_path}_intermediate_4.json"

cat "${base_path}_intermediate_4.json" | jq '.[] += {"protocol": "'"$protocol"'"}' > "${base_path}_final.json"
