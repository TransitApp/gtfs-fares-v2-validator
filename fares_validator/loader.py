from pathlib import Path

from . import read_gtfs_entities, read_fares_entities, diagnostics
from . import warnings as warn


class Entities:
    # Can eventually list the known types here for a typechecker like mypy
    pass


def run_validator(gtfs_root_dir, should_read_stop_times):
    gtfs_root_dir = Path(gtfs_root_dir)
    results = diagnostics.Diagnostics()

    gtfs = Entities()

    gtfs.areas = read_fares_entities.areas(gtfs_root_dir, results)

    gtfs.networks = read_gtfs_entities.networks(gtfs_root_dir, results)

    read_gtfs_entities.verify_stop_area_linkage(gtfs_root_dir, gtfs.areas, results, should_read_stop_times)

    gtfs.service_ids = read_gtfs_entities.service_ids(gtfs_root_dir, results)

    gtfs.timeframe_ids = read_fares_entities.timeframes(gtfs_root_dir, results)
    unused_timeframes = gtfs.timeframe_ids.copy()

    gtfs.rider_category_ids = read_fares_entities.rider_categories(gtfs_root_dir, results)

    gtfs.rider_category_by_fare_container = read_fares_entities.fare_containers(gtfs_root_dir,
                                                                                                 gtfs.rider_category_ids,
                                                                                                 results)

    gtfs.linked_entities_by_fare_product = read_fares_entities.fare_products(gtfs_root_dir,
                                                                                              gtfs,
                                                                                              unused_timeframes,
                                                                                              results)

    gtfs.leg_group_ids = read_fares_entities.fare_leg_rules(gtfs_root_dir, gtfs,
                                                                             unused_timeframes, results)

    read_fares_entities.fare_transfer_rules(gtfs_root_dir, gtfs, results)

    if len(unused_timeframes):
        warning_info = 'Unused timeframes: ' + str(unused_timeframes)
        results.add_warning(diagnostics.format(warn.UNUSED_TIMEFRAME_IDS, '', '', warning_info))

    return results
