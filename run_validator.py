from src import read_gtfs_entities, read_fares_entities

def run_validator(gtfs_root_dir, should_read_stop_times):
    errors = []
    warnings = []

    dependent_entities = {}

    dependent_entities['areas'] = read_gtfs_entities.areas(gtfs_root_dir, errors)
    dependent_entities['networks'] = read_gtfs_entities.networks(gtfs_root_dir, warnings)
    read_gtfs_entities.stop_areas(gtfs_root_dir, dependent_entities['areas'], errors, warnings, should_read_stop_times)
    dependent_entities['service_ids'] = read_gtfs_entities.service_ids(gtfs_root_dir, errors, warnings)
    dependent_entities['timeframe_ids'] = read_fares_entities.timeframes(gtfs_root_dir, errors)
    dependent_entities['rider_category_ids'] = read_fares_entities.rider_categories(gtfs_root_dir, errors, warnings)
    dependent_entities['rider_category_by_fare_container'] = read_fares_entities.fare_containers(gtfs_root_dir, dependent_entities['rider_category_ids'], errors)
    dependent_entities['linked_entities_by_fare_product'] = read_fares_entities.fare_products(gtfs_root_dir, dependent_entities, errors, warnings)
    dependent_entities['leg_group_ids'] = read_fares_entities.fare_leg_rules(gtfs_root_dir, dependent_entities, errors)
    read_fares_entities.fare_transfer_rules(gtfs_root_dir, dependent_entities, errors)

    return {
        'errors': errors, 
        'warnings': warnings
    }