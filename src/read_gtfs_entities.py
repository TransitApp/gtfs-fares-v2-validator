import csv
from os import path
from .utils import read_csv_file, check_areas_of_file

def areas(gtfs_root_dir, errors):
    greater_area_id_by_area_id = {}
    def for_each_area(line, line_num_error_msg):
        area_id = line.get('area_id')
        greater_area_id = line.get('greater_area_id')

        if area_id in greater_area_id_by_area_id:
            error_string = 'An area_id is defined twice in areas.txt: '
            error_string += area_id + line_num_error_msg
            errors.append(error_string)
            return

        if not area_id:
            errors.append('An entry in areas.txt has empty area id.' + line_num_error_msg)
            return

        greater_area_id_by_area_id[area_id] = greater_area_id
    
    areas_path = path.join(gtfs_root_dir, 'areas.txt')

    if not path.isfile(areas_path):
        return []

    read_csv_file(areas_path, ['area_id'], errors, for_each_area)

    for area_id in greater_area_id_by_area_id:
        greater_area_id = greater_area_id_by_area_id[area_id]

        while greater_area_id:
            if (greater_area_id == area_id):
                error_string = 'An area_id has itself as a greater_area_id: '
                error_string += area_id
                errors.append(error_string)
                break

            if not greater_area_id in greater_area_id_by_area_id:
                error_string = 'A greater_area_id is not defined as an area_id in areas.txt: '
                error_string += greater_area_id
                errors.append(error_string)
                break

            greater_area_id = greater_area_id_by_area_id[greater_area_id]

    return list(greater_area_id_by_area_id.keys())

def networks(gtfs_root_dir, warnings):
    routes_path = path.join(gtfs_root_dir, 'routes.txt')

    if not path.isfile(routes_path):
        warnings.append('No routes.txt was found, will assume no networks exist.')
        return []

    networks = []

    with open(routes_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        if not 'network_id' in reader.fieldnames:
            return networks

        for line in reader:
            network_id = line.get('network_id')
            
            if network_id and (not network_id in networks):
                networks.append(network_id)

    return networks

def stop_areas(gtfs_root_dir, areas, errors, warnings, should_read_stop_times):
    stops_path = path.join(gtfs_root_dir, 'stops.txt')
    stop_times_path = path.join(gtfs_root_dir, 'stop_times.txt')

    stops_exists = path.isfile(stops_path)
    stop_times_exists = False
    if should_read_stop_times:
        stop_times_exists = path.isfile(stop_times_path)

    if not stops_exists:
        warnings.append('No stops.txt was found. Will assume stops.txt does not reference any areas.') 
    if not stop_times_exists:
        warnings.append('No stop_times.txt was found. Will assume stop_times.txt does not reference any areas.')

    unused_areas = areas.copy()

    if stops_exists:
        check_areas_of_file(stops_path, 'stop', areas, unused_areas, errors)
    if stop_times_exists:
        check_areas_of_file(stop_times_path, 'stop_time', areas, unused_areas, errors)
    
    if len(unused_areas) > 0:
        warning_string = 'Areas defined in areas.txt are unused in stops.txt or stop_times.txt: '
        warning_string += str(unused_areas)
        warnings.append(warning_string)

def service_ids(gtfs_root_dir, errors, warnings):
    service_ids = []
    def for_each_calendar(line, line_num_error_msg):
        service_id = line.get('service_id')

        if not service_id:
            errors.append('calendar.txt includes a line with an empty service_id.' + line_num_error_msg)
            return

        if service_id in service_ids:
            error_string = 'calendar.txt includes more than one entry with the same service_id: '
            error_string += service_id + line_num_error_msg
            errors.append(error_string)

        service_ids.append(service_id)
    
    def for_each_calendar_date(line, line_num_error_msg):
        service_id = line.get('service_id')

        if service_id == '':
            errors.append('calendar_dates.txt includes a line with an empty service_id.' + line_num_error_msg)
            return

        if not service_id in service_ids:
            service_ids.append(service_id)

    calendar_path = path.join(gtfs_root_dir, 'calendar.txt')
    calendar_dates_path = path.join(gtfs_root_dir, 'calendar_dates.txt')
    
    calendar_exists = path.isfile(calendar_path)
    calendar_dates_exists = path.isfile(calendar_dates_path)

    if not calendar_exists and not calendar_dates_exists:
        warnings.append('Neither calendar.txt or calendar_dates.txt was found, will assume no service_ids for fares data.')
        return service_ids

    if calendar_exists:
        read_csv_file(calendar_path, ['service_id'], errors, for_each_calendar)

    if calendar_dates_exists:
        read_csv_file(calendar_dates_path, ['service_id'], errors, for_each_calendar_date)

    return service_ids