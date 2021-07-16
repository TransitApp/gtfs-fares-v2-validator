# Reads files introduced as part of the GTFS fares-v2 specification

import re
from os import path

from .utils import check_fare_amount, read_csv_file, check_linked_id, check_amts, check_linked_flr_ftr_entities
from .fare_product_checkers import check_linked_fp_entities, check_bundle, check_durations_and_offsets
from .fare_leg_rule_checkers import check_areas, check_distances
from .fare_transfer_rule_checkers import check_leg_groups, check_spans_and_transfer_ids, check_durations
from .errors import *
from .warnings import *

def areas(gtfs_root_dir, errors):
    greater_area_id_by_area_id = {}
    def for_each_area(line, line_num_error_msg):
        area_id = line.get('area_id')
        greater_area_id = line.get('greater_area_id')

        if area_id in greater_area_id_by_area_id:
            add_error(DUPLICATE_AREA_ID, line_num_error_msg, errors)
            return

        if not area_id:
            add_error(EMPTY_AREA_ID, line_num_error_msg, errors)
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
                error_info = 'area_id: ' + area_id
                add_error(GREATER_AREA_ID_LOOP, '', errors, '', error_info)
                break

            if not greater_area_id in greater_area_id_by_area_id:
                error_info = 'greater_area_id: ' + greater_area_id
                add_error(UNDEFINED_GREATER_AREA_ID, '', errors, '', error_info)
                break

            greater_area_id = greater_area_id_by_area_id[greater_area_id]

    return list(greater_area_id_by_area_id.keys())

def timeframes(gtfs_root_dir, errors):
    timeframes = []
    def for_each_timeframe(line, line_num_error_msg):
        timeframe_id = line.get('timeframe_id')
        start_time = line.get('start_time')
        end_time = line.get('end_time')

        if not timeframe_id:
            add_error(EMPTY_TIMEFRAME_ID, line_num_error_msg, errors)
            return
        if not start_time:
            add_error(EMPTY_START_TIME, line_num_error_msg, errors)
            return
        if not end_time:
            add_error(EMPTY_END_TIME, line_num_error_msg, errors)
            return

        starttimematch = re.search(r'^\d?\d:\d\d:\d\d$', start_time)
        endtimematch = re.search(r'^\d?\d:\d\d:\d\d$', end_time)

        if not starttimematch or not endtimematch:
            add_error(INVALID_TIME_FORMAT, line_num_error_msg, errors)
            timeframes.append(timeframe_id)
            return

        starttime_split = start_time.split(':')
        endtime_split = end_time.split(':')
        
        if int(starttime_split[0]) > 23 or int(endtime_split[0]) > 23:
            add_error(INVALID_TIME_FORMAT, line_num_error_msg, errors)

        if int(starttime_split[1]) > 59 or int(endtime_split[1]) > 59:
            add_error(INVALID_TIME_FORMAT, line_num_error_msg, errors)

        if int(starttime_split[2]) > 59 or int(endtime_split[2]) > 59:
            add_error(INVALID_TIME_FORMAT, line_num_error_msg, errors)

        if timeframe_id in timeframes:
            pass
        else:
            timeframes.append(timeframe_id)

    timeframes_path = path.join(gtfs_root_dir, 'timeframes.txt')

    if not path.isfile(timeframes_path):
        return timeframes

    read_csv_file(timeframes_path, ['timeframe_id', 'start_time', 'end_time'], errors, for_each_timeframe)

    return timeframes

def rider_categories(gtfs_root_dir, errors, warnings):
    rider_categories = []
    def for_each_rider_category(line, line_num_error_msg):
        rider_category = line.get('rider_category_id')
        min_age = line.get('min_age')
        min_age_int = 0
        max_age = line.get('max_age')

        if not rider_category:
            add_error(EMPTY_RIDER_CATEGORY_ID, line_num_error_msg, errors)
            return

        if not rider_category in rider_categories:
            rider_categories.append(rider_category)
        
        if min_age:
            try:
                min_age_int = int(min_age)
                if min_age_int < 0:
                    add_error(NEGATIVE_MIN_AGE, line_num_error_msg, errors)
                if min_age_int > 100:
                    add_warning(VERY_LARGE_MIN_AGE, line_num_error_msg, warnings)
            except ValueError:
                add_error(NON_INT_MIN_AGE, line_num_error_msg, errors)
        if max_age:
            try:
                max_age_int = int(max_age)
                if max_age_int < 0:
                    add_error(NEGATIVE_MAX_AGE, line_num_error_msg, errors)
                if max_age_int > 100:
                    add_warning(VERY_LARGE_MAX_AGE, line_num_error_msg, warnings)
                if max_age_int <= min_age_int:
                    add_warning(MAX_AGE_LESS_THAN_MIN_AGE, line_num_error_msg, warnings)
            except ValueError:
                add_error(NON_INT_MAX_AGE, line_num_error_msg, errors)

    rider_categories_path = path.join(gtfs_root_dir, 'rider_categories.txt')

    if not path.isfile(rider_categories_path):
        return rider_categories

    read_csv_file(rider_categories_path, ['rider_category_id'], errors, for_each_rider_category)

    return rider_categories

def fare_containers(gtfs_root_dir, rider_categories, errors):
    rider_category_by_fare_container = {}
    fare_containers_path = path.join(gtfs_root_dir, 'fare_containers.txt')

    def for_each_fare_container(line, line_num_error_msg):
        fare_container_id = line.get('fare_container_id')
        fare_container_name = line.get('fare_container_name')
        rider_category_id = line.get('rider_category_id')

        if not fare_container_id:
            add_error(EMPTY_FARE_CONTAINER_ID, line_num_error_msg, errors)
            return

        if not fare_container_name:
            add_error(EMPTY_FARE_CONTAINER_NAME, line_num_error_msg, errors)
            return

        amount_exists = check_fare_amount(fare_containers_path, line, line_num_error_msg, 'amount', 'currency', errors)
        min_purchase_exists = check_fare_amount(fare_containers_path, line, line_num_error_msg, 'minimum_initial_purchase', 'currency', errors)
        if (not amount_exists and not min_purchase_exists) and line.get('currency'):
            add_error(CURRENCY_WITHOUT_AMOUNT, line_num_error_msg, errors, 'fare_containers.txt')

        if fare_container_id in rider_category_by_fare_container:
            add_error(DUPLICATE_FARE_CONTAINER_ID, line_num_error_msg, errors)
            return

        if rider_category_id:
            if not rider_category_id in rider_categories:
                add_error(NONEXISTENT_RIDER_CATEGORY_ID, line_num_error_msg, errors, 'fare_containers.txt')

        rider_category_by_fare_container[fare_container_id] = rider_category_id
    
    if not path.isfile(fare_containers_path):
        return rider_category_by_fare_container

    read_csv_file(fare_containers_path, ['fare_container_id', 'fare_container_name'], errors, for_each_fare_container)

    return rider_category_by_fare_container

def fare_products(gtfs_root_dir, dependent_entities, unused_timeframes, errors, warnings):
    linked_entities_by_fare_product = {}
    
    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']

    fare_products_path = path.join(gtfs_root_dir, 'fare_products.txt')

    def for_each_fare_product(line, line_num_error_msg):
        if not line.get('fare_product_id'):
            add_error(EMPTY_FARE_PRODUCT_ID, line_num_error_msg, errors)
            return
        if not line.get('fare_product_name'):
            add_error(EMPTY_FARE_PRODUCT_NAME, line_num_error_msg, errors)
            return
        
        check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)

        min_amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            add_error(CURRENCY_WITHOUT_AMOUNT, line_num_error_msg, errors, 'fare_products.txt')
        check_amts(fare_products_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)

        check_bundle(line, line_num_error_msg, errors)
        check_linked_id(path, line, 'service_id', service_ids, line_num_error_msg, errors)
        timeframe_exists = check_linked_id(path, line, 'timeframe_id', timeframe_ids, line_num_error_msg, errors)
        if line.get('timeframe_id') in unused_timeframes:
            unused_timeframes.remove(line.get('timeframe_id'))
        if timeframe_exists:
            if not line.get('timeframe_type') in ['0', '1']:
                add_error(INVALID_TIMEFRAME_TYPE, line_num_error_msg, errors)
        else:
            if line.get('timeframe_type'):
                add_error(TIMEFRAME_TYPE_WITHOUT_TIMEFRAME, line_num_error_msg, errors)
        
        check_durations_and_offsets(line, line_num_error_msg, errors, warnings)

    if not path.isfile(fare_products_path):
        return linked_entities_by_fare_product
    
    read_csv_file(fare_products_path, ['fare_product_id', 'fare_product_name'], errors, for_each_fare_product)

    return linked_entities_by_fare_product

def fare_leg_rules(gtfs_root_dir, dependent_entities, unused_timeframes, errors, warnings):
    leg_group_ids = []

    areas =  dependent_entities['areas']
    unused_areas = areas.copy()
    networks =  dependent_entities['networks']
    unused_networks = networks.copy()
    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_leg_rules_path = path.join(gtfs_root_dir, 'fare_leg_rules.txt')

    def for_each_fare_leg_rule(line, line_num_error_msg):
        if line.get('leg_group_id') and not line.get('leg_group_id') in leg_group_ids:
            leg_group_ids.append(line.get('leg_group_id'))

        check_areas(fare_leg_rules_path, line, line_num_error_msg, areas, unused_areas, errors)
        check_linked_id(fare_leg_rules_path, line, 'network_id', networks, line_num_error_msg, errors)
        if line.get('network_id') in unused_networks:
            unused_networks.remove(line.get('network_id'))
        check_linked_id(fare_leg_rules_path, line, 'from_timeframe_id', timeframe_ids, line_num_error_msg, errors)
        if line.get('from_timeframe_id') in unused_timeframes:
            unused_timeframes.remove(line.get('from_timeframe_id'))
        check_linked_id(fare_leg_rules_path, line, 'to_timeframe_id', timeframe_ids, line_num_error_msg, errors)
        if line.get('to_timeframe_id') in unused_timeframes:
            unused_timeframes.remove(line.get('to_timeframe_id'))
        check_linked_id(fare_leg_rules_path, line, 'service_id', service_ids, line_num_error_msg, errors)
        check_distances(line, line_num_error_msg, errors)

        min_amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            add_error(CURRENCY_WITHOUT_AMOUNT, line_num_error_msg, errors, 'fare_leg_rules.txt')
        check_amts(fare_leg_rules_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)
        if (min_amt_exists or max_amt_exists or amt_exists) and line.get('fare_product_id'):
            add_error(AMOUNT_WITH_FARE_PRODUCT, line_num_error_msg, errors)
        
        if line.get('fare_leg_name') and line.get('fare_product_id'):
            add_error(FARE_LEG_NAME_WITH_FARE_PRODUCT, line_num_error_msg, errors)
        
        check_linked_flr_ftr_entities(fare_leg_rules_path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)
        
    if path.isfile(fare_leg_rules_path):
        read_csv_file(fare_leg_rules_path, [], errors, for_each_fare_leg_rule)    

    if len(unused_areas) > 0:
        warning_info = 'Unused areas: ' + str(unused_areas)
        add_warning(UNUSED_AREA_IDS, '', warnings, '', warning_info)
    if len(unused_networks) > 0:
        warning_info = 'Unused networks: ' + str(unused_networks)
        add_warning(UNUSED_NETWORK_IDS, '', warnings, '', warning_info)

    return leg_group_ids

def fare_transfer_rules(gtfs_root_dir, dependent_entities, errors, warnings):
    leg_group_ids = dependent_entities['leg_group_ids']
    unused_leg_groups = leg_group_ids.copy()
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_transfer_rules_path = path.join(gtfs_root_dir, 'fare_transfer_rules.txt')

    def for_each_fare_transfer_rule(line, line_num_error_msg):
        check_leg_groups(line, line_num_error_msg, leg_group_ids, unused_leg_groups, errors)
        check_spans_and_transfer_ids(line, line_num_error_msg, errors)
        check_durations(line, line_num_error_msg, errors)

        min_amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            add_error(CURRENCY_WITHOUT_AMOUNT, line_num_error_msg, errors, 'fare_transfer_rules.txt')
        check_amts(fare_transfer_rules_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)

        if (min_amt_exists or max_amt_exists or amt_exists) and not line.get('fare_transfer_type'):
            add_error(AMOUNT_WITHOUT_FARE_TRANSFER_TYPE, line_num_error_msg, errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('fare_transfer_type'):
            add_error(FARE_TRANSFER_TYPE_WITHOUT_AMOUNT, line_num_error_msg, errors)
        if line.get('fare_transfer_type') and (line.get('fare_transfer_type') not in ['0', '1', '2', '3']):
            add_error(INVALID_FARE_TRANSFER_TYPE, line_num_error_msg, errors)
        
        check_linked_flr_ftr_entities(fare_transfer_rules_path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)
    
    if path.isfile(fare_transfer_rules_path):
        read_csv_file(fare_transfer_rules_path, [], errors, for_each_fare_transfer_rule)

    if len(unused_leg_groups) > 0:
        warning_info = 'Unused leg groups: ' + str(unused_leg_groups)
        add_warning(UNUSED_LEG_GROUPS, '', warnings, '', warning_info)