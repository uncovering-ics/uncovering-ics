#!/bin/bash
set -eu

data_dir="$1"
aggregated_dir="${data_dir}/aggregated"

echo "Aggregated data destination directory: ${aggregated_dir}"

mkdir ${aggregated_dir}

echo "Generating all_ases.txt"
cat "${data_dir}"/*_final.json | jq '.[] | .asn' | sort -V | uniq | awk '{print "AS" $0}' > "${aggregated_dir}/all_ases.txt"


echo "Generating per-protocol graphs"
for protocol in S7 MODBUS DNP3 BACNET EIP FOX IEC60870_5_104 ATG CODESYS FINS GE_SRTP HART MMS OPC_UA PCWORX PRO_CON_OS WDBRPC
do
    ./other/classifications.py <(cat "${data_dir}/"*_"${protocol}"_*_final.json | jq -a '.[]' | jq -s) "${aggregated_dir}/all_${protocol}_classifications.pdf" &>/dev/null
done

echo "Aggregating results into temporary files"
cat "${data_dir}"/*_final.json | jq '.[]' | jq -s > "${aggregated_dir}/all_final.tmp.json"
cat "${aggregated_dir}/all_final.tmp.json" | jq '.[] | select(.classification == "honeypot_medium_confidence" or .classification == "honeypot_high_confidence")' | jq -s > "${aggregated_dir}/all_final_honeypot.tmp.json"
cat "${aggregated_dir}/all_final.tmp.json" | jq '.[] | select(.classification == "potentially_real")' | jq -s > "${aggregated_dir}/all_final_real.tmp.json"

echo "Generating general_stats.txt"
./other/general_stats.py "${aggregated_dir}/all_final.tmp.json" > "${aggregated_dir}/general_stats.txt"

echo "Generating classifications_per_as.txt"
./other/classifications_per_as.py "${aggregated_dir}/all_final.tmp.json" > "${aggregated_dir}/classifications_per_as.txt"

echo "Generating classifications per country map and plot"
./other/classifications_per_country_map.py "${aggregated_dir}/all_final.tmp.json" "$aggregated_dir/classifications_per_country.pdf" "$aggregated_dir/classifications_per_country_top15.pdf" > "${aggregated_dir}/classifications_per_country.txt"

echo "Generating open port cdf"
./other/open_port_cdf.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/open_port_cdf.pdf" "${aggregated_dir}/open_port_cdf_honeypots.pdf" > "${aggregated_dir}/open_port_proportions.txt"

echo "Generating per-protocol open port cdf"
./other/protocol_open_port_cdf.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/protocol_open_port_cdf.pdf" solid

echo "Generating per-protocol open port cdf for honeypots"
./other/protocol_open_port_cdf.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/protocol_open_port_cdf_honeypot.pdf" dashed

echo "Generating AS type host count cdf for honeypots"
./other/as_type_count_cdf.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/as_type_count_cdf_honeypot.pdf"

echo "Generating per-protocol open port cdf for datacenters"
./other/protocol_open_port_cdf.py <(cat "${aggregated_dir}/all_final.tmp.json" | jq '.[] | select([.indications[] | (contains("as_hosting") or contains("company_hosting"))] | any)' | jq -s) "${aggregated_dir}/protocol_open_port_cdf_datacenter.pdf" dashdot

echo "Generating country pie chart"
./other/country_pie_chart.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/pie_chart_country_all.pdf"

echo "Generating AS pie chart"
./other/as_pie_chart.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/pie_chart_as_all.pdf"

echo "Generating honeypot country pie chart"
./other/country_pie_chart.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/pie_chart_country_honeypot.pdf"

echo "Generating company type pie chart"
./other/company_type_pie_chart.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/pie_chart_company_type_all.pdf"

echo "Generating real company type pie chart"
./other/company_type_pie_chart.py "${aggregated_dir}/all_final_real.tmp.json" "${aggregated_dir}/pie_chart_company_type_real.pdf"

echo "Generating honeypot company type pie chart"
./other/company_type_pie_chart.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/pie_chart_company_type_honeypot.pdf"

echo "Generating honeypot AS pie chart"
./other/as_pie_chart.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/pie_chart_as_honeypot.pdf"

echo "Generating real country pie chart"
./other/country_pie_chart.py "${aggregated_dir}/all_final_real.tmp.json" "${aggregated_dir}/pie_chart_country_real.pdf"

echo "Generating real AS pie chart"
./other/as_pie_chart.py "${aggregated_dir}/all_final_real.tmp.json" "${aggregated_dir}/pie_chart_as_real.pdf"

echo "Generating real distribution map"
./other/total_per_country_map.py "${aggregated_dir}/all_final_real.tmp.json" "Blues" "${aggregated_dir}/total_per_country_real.pdf"

echo "Generating honeypot distribution map"
./other/total_per_country_map.py "${aggregated_dir}/all_final_honeypot.tmp.json" "YlOrRd" "${aggregated_dir}/total_per_country_honeypot.pdf"

echo "Generating honeypot protocol popularity map"
./other/protocol_popularity_map.py "${aggregated_dir}/all_final_honeypot.tmp.json" "${aggregated_dir}/protocol_popularity_honeypot.pdf" "${aggregated_dir}/protocol_popularity_top10_honeypot.pdf" > "${aggregated_dir}/protocol_popularity_honeypot.txt"

echo "Generating non-honeypot protocol popularity map"
./other/protocol_popularity_map.py "${aggregated_dir}/all_final_real.tmp.json" "${aggregated_dir}/protocol_popularity_real.pdf" "${aggregated_dir}/protocol_popularity_top10_real.pdf" > "${aggregated_dir}/protocol_popularity_real.txt"

echo "Generating indication correlation matrix"
./other/indication_correlation_heatmap.py "${aggregated_dir}/all_final.tmp.json" "${aggregated_dir}/indication_correlation_heatmap.pdf"

echo "Generating honeypot protocol count"
./other/protocol_count.py "${aggregated_dir}/all_final_honeypot.tmp.json" honeypot "${aggregated_dir}/protocol_count_honeypot.pdf"

echo "Generating real protocol count"
./other/protocol_count.py "${aggregated_dir}/all_final_real.tmp.json" real "${aggregated_dir}/protocol_count_real.pdf"

echo "Generating honeypot AS protocol count"
./other/protocol_count_as.py "${aggregated_dir}/all_final_honeypot.tmp.json" honeypot "${aggregated_dir}/protocol_count_as_honeypot.pdf"

echo "Generating real AS protocol count"
./other/protocol_count_as.py "${aggregated_dir}/all_final_real.tmp.json" real "${aggregated_dir}/protocol_count_as_real.pdf"

echo "Generating protocol correlations"
./other/protocol_correlations.py "${aggregated_dir}/all_final.tmp.json" > "${aggregated_dir}/protocol_correlations.txt"

echo "Generating real protocol correlations"
./other/protocol_correlations.py "${aggregated_dir}/all_final_real.tmp.json" > "${aggregated_dir}/protocol_correlations_real.txt"

echo "Generating honeypot protocol correlations"
./other/protocol_correlations.py "${aggregated_dir}/all_final_honeypot.tmp.json" > "${aggregated_dir}/protocol_correlations_honeypot.txt"

echo "Generating company_list.csv"
./other/company_list.py "${aggregated_dir}/all_final.tmp.json" > "${aggregated_dir}/company_list.csv"

echo "Cleaning up"
rm "${aggregated_dir}/all_final.tmp.json"
rm "${aggregated_dir}/all_final_honeypot.tmp.json"
rm "${aggregated_dir}/all_final_real.tmp.json"
