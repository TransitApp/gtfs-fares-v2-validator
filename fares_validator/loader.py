from pathlib import Path

from . import read_gtfs_entities, read_fares_entities, diagnostics
from . import warnings as warn


class Entities:
    # Can eventually list the known types here for a typechecker like mypy
    pass


def run_validator(gtfs_root_dir, experimental=True):
    gtfs_root_dir = Path(gtfs_root_dir)
    results = diagnostics.Diagnostics()

    gtfs = Entities()

    gtfs.areas = read_fares_entities.areas(gtfs_root_dir, results)

    stops = read_gtfs_entities.stops(gtfs_root_dir, results)

    read_fares_entities.stop_areas(gtfs_root_dir, results, gtfs.areas, stops)

    gtfs.networks = read_gtfs_entities.networks(gtfs_root_dir, results)

    gtfs.service_ids = read_gtfs_entities.service_ids(gtfs_root_dir, results)

    unused_timeframes = set()
    if (experimental):
        gtfs.timeframe_ids = read_fares_entities.timeframes(
            gtfs_root_dir, results)
        unused_timeframes = gtfs.timeframe_ids.copy()

    if (experimental):
        gtfs.rider_category_ids = read_fares_entities.rider_categories(
            gtfs_root_dir, results)

    if (experimental):
        gtfs.rider_category_by_fare_container = read_fares_entities.fare_containers(
            gtfs_root_dir, gtfs.rider_category_ids, results)

    gtfs.linked_entities_by_fare_product = read_fares_entities.fare_products(
        gtfs_root_dir, gtfs, results, experimental)

    gtfs.leg_group_ids = read_fares_entities.fare_leg_rules(
        gtfs_root_dir, gtfs, unused_timeframes, results, experimental)

    read_fares_entities.fare_transfer_rules(gtfs_root_dir, gtfs, results,
                                            experimental)

    if len(unused_timeframes):
        warning_info = 'Unused timeframes: ' + str(unused_timeframes)
        results.add_warning(
            diagnostics.format(warn.UNUSED_TIMEFRAME_IDS, '', '', warning_info))

    return results
