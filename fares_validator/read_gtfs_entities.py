"""
Reads files introduced as part of the original GTFS specification
"""

from . import diagnostics, utils
from .errors import *
from .warnings import *


def networks(gtfs_root_dir, messages):
    networks = set()

    for line in utils.read_csv_file(gtfs_root_dir / 'routes.txt', [], [], messages, NO_ROUTES):
        if line.network_id:
                networks.add(line.network_id)

    return networks


def stop_areas(gtfs_root_dir, areas, messages, should_read_stop_times):
    stops_path = gtfs_root_dir / 'stops.txt'
    stop_times_path = gtfs_root_dir / 'stop_times.txt'

    unused_areas = areas.copy()

    if stops_path.exists():
        utils.check_areas_of_file(stops_path, 'stop', areas, unused_areas, messages)
    else:
        messages.add_warning(diagnostics.format(NO_STOPS, ''))

    if should_read_stop_times and stop_times_path.exists():
        utils.check_areas_of_file(stop_times_path, 'stop_time', areas, unused_areas, messages)

    if len(unused_areas):
        messages.add_warning(diagnostics.format(UNUSED_AREAS_IN_STOPS, '', '', f'Unused areas: {unused_areas}'))


def service_ids(gtfs_root_dir, messages):
    calendar_path = gtfs_root_dir / 'calendar.txt'
    calendar_dates_path = gtfs_root_dir / 'calendar_dates.txt'

    service_ids = set()
    if not calendar_path.exists() and not calendar_dates_path.exists():
        messages.add_warning(diagnostics.format(NO_SERVICE_IDS, ''))
        return service_ids

    for line in utils.read_csv_file(calendar_path, ['service_id'], [], messages):
        if not line.service_id:
            line.add_error(EMPTY_SERVICE_ID_CALENDAR)
            continue

        if line.service_id in service_ids:
            line.add_error(DUPLICATE_SERVICE_ID, f'service_id: {line.service_id}')

        service_ids.add(line.service_id)

    for line in utils.read_csv_file(calendar_dates_path, ['service_id'], [], messages):
        if not line.service_id:
            line.add_error(EMPTY_SERVICE_ID_CALENDAR_DATES)
            continue

        service_ids.add(line.service_id)

    return service_ids
