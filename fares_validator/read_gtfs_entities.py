"""
Reads files introduced as part of the original GTFS specification
"""

import csv
from os import path
from .utils import read_csv_file, check_areas_of_file
from .errors import *
from .warnings import *

def networks(gtfs_root_dir, messages):
    routes_path = path.join(gtfs_root_dir, 'routes.txt')

    if not path.isfile(routes_path):
        messages.add_warning(NO_ROUTES, '')
        return []

    networks = []

    with open(routes_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        if 'network_id' not in reader.fieldnames:
            return networks

        for line in reader:
            network_id = line.get('network_id')
            
            if network_id and network_id not in networks:
                networks.append(network_id)

    return networks

def stop_areas(gtfs_root_dir, areas, messages, should_read_stop_times):
    stops_path = path.join(gtfs_root_dir, 'stops.txt')
    stop_times_path = path.join(gtfs_root_dir, 'stop_times.txt')

    stops_exists = path.isfile(stops_path)
    stop_times_exists = False
    if should_read_stop_times:
        stop_times_exists = path.isfile(stop_times_path)

    if not stops_exists:
        messages.add_warning(NO_STOPS, '')

    unused_areas = areas.copy()

    if stops_exists:
        check_areas_of_file(stops_path, 'stop', areas, unused_areas, messages)
    if stop_times_exists:
        check_areas_of_file(stop_times_path, 'stop_time', areas, unused_areas, messages)
    
    if len(unused_areas) > 0:
        warning_info = 'Unused areas: ' + str(unused_areas)
        messages.add_warning(UNUSED_AREAS_IN_STOPS, '', '', warning_info)

def service_ids(gtfs_root_dir, messages):
    calendar_path = gtfs_root_dir / 'calendar.txt'
    calendar_dates_path = gtfs_root_dir / 'calendar_dates.txt'

    service_ids = []
    if not calendar_path.exists() and not calendar_dates_path.exists():
        messages.add_warning(NO_SERVICE_IDS, '')
        return service_ids

    for line in read_csv_file(calendar_path, ['service_id'], [], messages):
        if not line.service_id:
            messages.add_error(EMPTY_SERVICE_ID_CALENDAR, line.line_num_error_msg)
            continue

        if line.service_id in service_ids:
            error_info = 'service_id: ' + line.service_id
            messages.add_error(DUPLICATE_SERVICE_ID, line.line_num_error_msg, '', error_info)

        service_ids.append(line.service_id)

    for line in read_csv_file(calendar_dates_path, ['service_id'], [], messages):
        if not line.service_id:
            messages.add_error(EMPTY_SERVICE_ID_CALENDAR_DATES, line.line_num_error_msg)
            continue

        if line.service_id not in service_ids:
            service_ids.append(line.service_id)

    return service_ids
