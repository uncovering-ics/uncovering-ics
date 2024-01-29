#!/bin/sh
set -eu

censys search "services.service_name=$3 and location.country_code=$2" --pages -1 --fields "service_count" "autonomous_system.asn" "autonomous_system.name" "dns.reverse_dns.names" "location.country_code" "services.s7.copyright" "services.s7.cpu_profile" "services.s7.firmware" "services.s7.hardware" "services.s7.location" "services.s7.memory_serial_number" "services.s7.module" "services.s7.module_id" "services.s7.module_type" "services.s7.oem_id" "services.s7.plant_id" "services.s7.reserved_for_os" "services.s7.serial_number" "services.s7.system" -o "${1}/${2}_${3}_${4}_censys.json"
