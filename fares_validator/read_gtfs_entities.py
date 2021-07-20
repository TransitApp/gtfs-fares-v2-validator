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
    service_ids = []
    def for_each_calendar(line, line_num_error_msg):
        service_id = line.get('service_id')

        if not service_id:
            messages.add_error(EMPTY_SERVICE_ID_CALENDAR, line_num_error_msg)
            return

        if service_id in service_ids:
            error_info = 'service_id: ' + service_id
            messages.add_error(DUPLICATE_SERVICE_ID, line_num_error_msg, '', error_info)

        service_ids.append(service_id)
    
    def for_each_calendar_date(line, line_num_error_msg):
        service_id = line.get('service_id')

        if service_id == '':
            messages.add_error(EMPTY_SERVICE_ID_CALENDAR_DATES, line_num_error_msg)
            return

        if service_id not in service_ids:
            service_ids.append(service_id)

    calendar_path = path.join(gtfs_root_dir, 'calendar.txt')
    calendar_dates_path = path.join(gtfs_root_dir, 'calendar_dates.txt')
    
    calendar_exists = path.isfile(calendar_path)
    calendar_dates_exists = path.isfile(calendar_dates_path)

    if not calendar_exists and not calendar_dates_exists:
        messages.add_warning(NO_SERVICE_IDS, '')
        return service_ids

    if calendar_exists:
        read_csv_file(calendar_path, ['service_id'], [], messages, for_each_calendar)

    if calendar_dates_exists:
        read_csv_file(calendar_dates_path, ['service_id'], [], messages, for_each_calendar_date)

    return service_ids
