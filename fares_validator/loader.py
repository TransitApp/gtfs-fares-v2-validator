from . import read_gtfs_entities, read_fares_entities, messages
from . import warnings as warn

def run_validator(gtfs_root_dir, should_read_stop_times):
    results = messages.Messages()

    dependent_entities = {}

    dependent_entities['areas'] = read_fares_entities.areas(gtfs_root_dir, results)

    dependent_entities['networks'] = read_gtfs_entities.networks(gtfs_root_dir, results)

    read_gtfs_entities.stop_areas(gtfs_root_dir, dependent_entities['areas'], results, should_read_stop_times)

    dependent_entities['service_ids'] = read_gtfs_entities.service_ids(gtfs_root_dir, results)

    dependent_entities['timeframe_ids'] = read_fares_entities.timeframes(gtfs_root_dir, results)
    unused_timeframes = dependent_entities['timeframe_ids'].copy()

    dependent_entities['rider_category_ids'] = read_fares_entities.rider_categories(gtfs_root_dir, results)

    dependent_entities['rider_category_by_fare_container'] = read_fares_entities.fare_containers(gtfs_root_dir, dependent_entities['rider_category_ids'], results)

    dependent_entities['linked_entities_by_fare_product'] = read_fares_entities.fare_products(gtfs_root_dir, dependent_entities, unused_timeframes, results)

    dependent_entities['leg_group_ids'] = read_fares_entities.fare_leg_rules(gtfs_root_dir, dependent_entities, unused_timeframes, results)

    read_fares_entities.fare_transfer_rules(gtfs_root_dir, dependent_entities, results)

    if len(unused_timeframes):
        warning_info = 'Unused timeframes: ' + str(unused_timeframes)
        results.add_warning(warn.UNUSED_TIMEFRAME_IDS, '', '', warning_info)

    return results
