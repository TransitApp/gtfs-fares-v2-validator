"""
Reads files introduced as part of the original GTFS specification
"""

from . import diagnostics, utils, schema
from .errors import *
from .warnings import *


def networks(gtfs_root_dir, messages):
    networks = set()

    for line in utils.read_csv_file(gtfs_root_dir, schema.ROUTES, messages):
        if line.network_id:
            networks.add(line.network_id)

    return networks


def stops(gtfs_root_dir, messages):
    stop_ids = set()

    for line in utils.read_csv_file(gtfs_root_dir, schema.STOPS, messages):
        if line.stop_id:
            stop_ids.add(line.stop_id)

    return stop_ids

def service_ids(gtfs_root_dir, messages):
    service_ids = set()
    if not (gtfs_root_dir / 'calendar.txt').exists() and not (gtfs_root_dir / 'calendar_dates.txt').exists():
        messages.add_warning(diagnostics.format(NO_SERVICE_IDS, ''))
        return service_ids

    for line in utils.read_csv_file(gtfs_root_dir, schema.CALENDAR, messages):
        if not line.service_id:
            line.add_error(EMPTY_SERVICE_ID_CALENDAR)
            continue

        if line.service_id in service_ids:
            line.add_error(DUPLICATE_SERVICE_ID, f'service_id: {line.service_id}')

        service_ids.add(line.service_id)

    for line in utils.read_csv_file(gtfs_root_dir, schema.CALENDAR_DATES, messages):
        if not line.service_id:
            line.add_error(EMPTY_SERVICE_ID_CALENDAR_DATES)
            continue

        service_ids.add(line.service_id)

    return service_ids
