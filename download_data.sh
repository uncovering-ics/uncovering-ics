#!/bin/sh
set -eu

censys search "services.service_name=$3 and location.country_code=$2" --pages -1 --fields "service_count" "autonomous_system.asn" "autonomous_system.name" "dns.reverse_dns.names" "location.country_code" "services.s7.plant_id" "services.s7.reserved_for_os" "services.s7.serial_number" "services.s7.system" "services.port" "services.service_name" "services.banner_hex" "services.banner_hashes" "services.http.response.html_tags" "services.http.response.body_size" "services.http.response.body_hash" -o "${1}/${2}_${3}_${4}_censys.json"
