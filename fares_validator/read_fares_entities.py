# Reads files introduced as part of the GTFS fares-v2 specification

import re
from os import path

from . import defined_fields
from .errors import *
from .fare_leg_rule_checkers import check_areas, check_distances
from .fare_product_checkers import check_linked_fp_entities, check_bundle, check_durations_and_offsets
from .fare_transfer_rule_checkers import check_leg_groups, check_spans_and_transfer_ids, check_durations
from .utils import check_fare_amount, read_csv_file, check_linked_id, check_amts, check_linked_flr_ftr_entities
from .warnings import *


def areas(gtfs_root_dir, messages):
    greater_area_id_by_area_id = {}
    areas_path = gtfs_root_dir / 'areas.txt'

    if not areas_path.exists():
        messages.add_warning(NO_AREAS, '')
        return []

    for line in read_csv_file(areas_path, ['area_id'], defined_fields.AREAS, messages):
        if line.area_id in greater_area_id_by_area_id:
            messages.add_error(DUPLICATE_AREA_ID, line.line_num_error_msg)
            continue

        if not line.area_id:
            messages.add_error(EMPTY_AREA_ID, line.line_num_error_msg)
            continue

        greater_area_id_by_area_id[line.area_id] = line.greater_area_id

    for area_id in greater_area_id_by_area_id:
        greater_area_id = greater_area_id_by_area_id[area_id]

        while greater_area_id:
            if greater_area_id == area_id:
                error_info = 'area_id: ' + area_id
                messages.add_error(GREATER_AREA_ID_LOOP, '', '', error_info)
                break

            if greater_area_id not in greater_area_id_by_area_id:
                error_info = 'greater_area_id: ' + greater_area_id
                messages.add_error(UNDEFINED_GREATER_AREA_ID, '', '', error_info)
                break

            greater_area_id = greater_area_id_by_area_id[greater_area_id]

    return list(greater_area_id_by_area_id.keys())


def timeframes(gtfs_root_dir, messages):
    timeframes = []
    timeframes_path = gtfs_root_dir / 'timeframes.txt'

    if not timeframes_path.exists():
        messages.add_warning(NO_TIMEFRAMES, '')
        return timeframes

    for line in read_csv_file(timeframes_path, ['timeframe_id', 'start_time', 'end_time'], defined_fields.TIMEFRAMES,
                              messages):
        if not line.timeframe_id:
            messages.add_error(EMPTY_TIMEFRAME_ID, line.line_num_error_msg)
            continue
        if not line.start_time:
            messages.add_error(EMPTY_START_TIME, line.line_num_error_msg)
            continue
        if not line.end_time:
            messages.add_error(EMPTY_END_TIME, line.line_num_error_msg)
            continue

        starttimematch = re.search(r'^\d?\d:\d\d:\d\d$', line.start_time)
        endtimematch = re.search(r'^\d?\d:\d\d:\d\d$', line.end_time)

        if not starttimematch or not endtimematch:
            messages.add_error(INVALID_TIME_FORMAT, line.line_num_error_msg)
            timeframes.append(line.timeframe_id)
            continue

        starttime_split = line.start_time.split(':')
        endtime_split = line.end_time.split(':')

        if int(starttime_split[0]) > 23 or int(endtime_split[0]) > 23:
            messages.add_error(INVALID_TIME_FORMAT, line.line_num_error_msg)

        if int(starttime_split[1]) > 59 or int(endtime_split[1]) > 59:
            messages.add_error(INVALID_TIME_FORMAT, line.line_num_error_msg)

        if int(starttime_split[2]) > 59 or int(endtime_split[2]) > 59:
            messages.add_error(INVALID_TIME_FORMAT, line.line_num_error_msg)

        if line.timeframe_id not in timeframes:
            timeframes.append(line.timeframe_id)

    return timeframes


def rider_categories(gtfs_root_dir, messages):
    rider_categories = []
    rider_categories_path = gtfs_root_dir / 'rider_categories.txt'

    if not rider_categories_path.exists():
        messages.add_warning(NO_RIDER_CATEGORIES, '')
        return rider_categories

    for line in read_csv_file(rider_categories_path, ['rider_category_id'], defined_fields.RIDER_CATEGORIES, messages):
        min_age_int = 0
        if not line.rider_category_id:
            messages.add_error(EMPTY_RIDER_CATEGORY_ID, line.line_num_error_msg)
            continue

        if line.rider_category_id not in rider_categories:
            rider_categories.append(line.rider_category_id)

        if line.min_age:
            try:
                min_age_int = int(line.min_age)
                if min_age_int < 0:
                    messages.add_error(NEGATIVE_MIN_AGE, line.line_num_error_msg)
                if min_age_int > 100:
                    messages.add_warning(VERY_LARGE_MIN_AGE, line.line_num_error_msg)
            except ValueError:
                messages.add_error(NON_INT_MIN_AGE, line.line_num_error_msg)
        if line.max_age:
            try:
                max_age_int = int(line.max_age)
                if max_age_int < 0:
                    messages.add_error(NEGATIVE_MAX_AGE, line.line_num_error_msg)
                if max_age_int > 100:
                    messages.add_warning(VERY_LARGE_MAX_AGE, line.line_num_error_msg)
                if max_age_int <= min_age_int:
                    messages.add_warning(MAX_AGE_LESS_THAN_MIN_AGE, line.line_num_error_msg)
            except ValueError:
                messages.add_error(NON_INT_MAX_AGE, line.line_num_error_msg)

    return rider_categories


def fare_containers(gtfs_root_dir, rider_categories, messages):
    rider_category_by_fare_container = {}
    fare_containers_path = gtfs_root_dir / 'fare_containers.txt'

    if not fare_containers_path.exists():
        messages.add_warning(NO_FARE_CONTAINERS, '')
        return rider_category_by_fare_container

    for line in read_csv_file(fare_containers_path, ['fare_container_id', 'fare_container_name'],
                              defined_fields.FARE_CONTAINERS, messages):
        if not line.fare_container_id:
            messages.add_error(EMPTY_FARE_CONTAINER_ID, line.line_num_error_msg)
            continue

        if not line.fare_container_name:
            messages.add_error(EMPTY_FARE_CONTAINER_NAME, line.line_num_error_msg)
            continue

        amount_exists = check_fare_amount(fare_containers_path, line, 'amount', 'currency', messages)
        min_purchase_exists = check_fare_amount(fare_containers_path, line, 'minimum_initial_purchase', 'currency',
                                                messages)
        if (not amount_exists and not min_purchase_exists) and line.currency:
            messages.add_error(CURRENCY_WITHOUT_AMOUNT, line.line_num_error_msg, 'fare_containers.txt')

        if line.fare_container_id in rider_category_by_fare_container:
            messages.add_error(DUPLICATE_FARE_CONTAINER_ID, line.line_num_error_msg)
            continue

        if line.rider_category_id:
            if line.rider_category_id not in rider_categories:
                messages.add_error(NONEXISTENT_RIDER_CATEGORY_ID, line.line_num_error_msg, 'fare_containers.txt')

        rider_category_by_fare_container[line.fare_container_id] = line.rider_category_id

    return rider_category_by_fare_container


def fare_products(gtfs_root_dir, dependent_entities, unused_timeframes, messages):
    linked_entities_by_fare_product = {}

    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']

    fare_products_path = gtfs_root_dir / 'fare_products.txt'

    if not path.isfile(fare_products_path):
        messages.add_warning(NO_FARE_PRODUCTS, '')
        return linked_entities_by_fare_product

    for line in read_csv_file(fare_products_path, ['fare_product_id', 'fare_product_name'],
                              defined_fields.FARE_PRODUCTS, messages):
        if not line.fare_product_id:
            messages.add_error(EMPTY_FARE_PRODUCT_ID, line.line_num_error_msg)
            continue
        if not line.fare_product_name:
            messages.add_error(EMPTY_FARE_PRODUCT_NAME, line.line_num_error_msg)
            continue

        check_linked_fp_entities(line, rider_categories, rider_category_by_fare_container,
                                 linked_entities_by_fare_product, messages)

        min_amt_exists = check_fare_amount(fare_products_path, line, 'min_amount', 'currency', messages)
        max_amt_exists = check_fare_amount(fare_products_path, line, 'max_amount', 'currency', messages)
        amt_exists = check_fare_amount(fare_products_path, line, 'amount', 'currency', messages)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            messages.add_error(CURRENCY_WITHOUT_AMOUNT, line.line_num_error_msg, 'fare_products.txt')

        check_amts(fare_products_path, line, min_amt_exists, max_amt_exists, amt_exists, messages)

        check_bundle(line, messages)
        check_linked_id(fare_products_path, line, 'service_id', service_ids, messages)
        timeframe_exists = check_linked_id(fare_products_path, line, 'timeframe_id', timeframe_ids, messages)

        if line.timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.timeframe_id)
        if timeframe_exists:
            if line.timeframe_type not in {'0', '1'}:
                messages.add_error(INVALID_TIMEFRAME_TYPE, line.line_num_error_msg)
        else:
            if line.timeframe_type:
                messages.add_error(TIMEFRAME_TYPE_WITHOUT_TIMEFRAME, line.line_num_error_msg)

        check_durations_and_offsets(line, messages)

    return linked_entities_by_fare_product


def fare_leg_rules(gtfs_root_dir, dependent_entities, unused_timeframes, messages):
    leg_group_ids = []

    areas = dependent_entities['areas']
    unused_areas = areas.copy()
    networks = dependent_entities['networks']
    unused_networks = networks.copy()
    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_leg_rules_path = gtfs_root_dir / 'fare_leg_rules.txt'

    if not fare_leg_rules_path.exists():
        messages.add_warning(NO_FARE_LEG_RULES, '')

    for line in read_csv_file(fare_leg_rules_path, [], defined_fields.FARE_LEG_RULES, messages):
        if line.leg_group_id and line.leg_group_id not in leg_group_ids:
            leg_group_ids.append(line.leg_group_id)

        check_areas(fare_leg_rules_path, line, areas, unused_areas, messages)

        check_linked_id(fare_leg_rules_path, line, 'network_id', networks, messages)
        if line.network_id in unused_networks:
            unused_networks.remove(line.network_id)

        check_linked_id(fare_leg_rules_path, line, 'from_timeframe_id', timeframe_ids, messages)
        if line.from_timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.from_timeframe_id)
        check_linked_id(fare_leg_rules_path, line, 'to_timeframe_id', timeframe_ids, messages)
        if line.to_timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.to_timeframe_id)

        check_linked_id(fare_leg_rules_path, line, 'service_id', service_ids, messages)

        check_distances(line, messages)

        min_amt_exists = check_fare_amount(fare_leg_rules_path, line, 'min_amount', 'currency', messages)
        max_amt_exists = check_fare_amount(fare_leg_rules_path, line, 'max_amount', 'currency', messages)
        amt_exists = check_fare_amount(fare_leg_rules_path, line, 'amount', 'currency', messages)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            messages.add_error(CURRENCY_WITHOUT_AMOUNT, line.line_num_error_msg, 'fare_leg_rules.txt')
        check_amts(fare_leg_rules_path, line, min_amt_exists, max_amt_exists, amt_exists, messages)
        if (min_amt_exists or max_amt_exists or amt_exists) and line.fare_product_id:
            messages.add_error(AMOUNT_WITH_FARE_PRODUCT, line.line_num_error_msg)

        if line.fare_leg_name and line.fare_product_id:
            messages.add_error(FARE_LEG_NAME_WITH_FARE_PRODUCT, line.line_num_error_msg)

        check_linked_flr_ftr_entities(fare_leg_rules_path, line, rider_categories, rider_category_by_fare_container,
                                      linked_entities_by_fare_product, messages)

    if len(unused_areas):
        warning_info = 'Unused areas: ' + str(unused_areas)
        messages.add_warning(UNUSED_AREA_IDS, '', '', warning_info)

    if len(unused_networks):
        warning_info = 'Unused networks: ' + str(unused_networks)
        messages.add_warning(UNUSED_NETWORK_IDS, '', '', warning_info)

    return leg_group_ids


def fare_transfer_rules(gtfs_root_dir, dependent_entities, messages):
    leg_group_ids = dependent_entities['leg_group_ids']
    unused_leg_groups = leg_group_ids.copy()
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_transfer_rules_path = gtfs_root_dir / 'fare_transfer_rules.txt'

    if not fare_transfer_rules_path.exists():
        messages.add_warning(NO_FARE_TRANSFER_RULES, '')

    for line in read_csv_file(fare_transfer_rules_path, [], defined_fields.FARE_TRANSFER_RULES, messages):
        check_leg_groups(line, leg_group_ids, unused_leg_groups, messages)
        check_spans_and_transfer_ids(line, messages)
        check_durations(line, messages)

        min_amt_exists = check_fare_amount(fare_transfer_rules_path, line, 'min_amount', 'currency', messages)
        max_amt_exists = check_fare_amount(fare_transfer_rules_path, line, 'max_amount', 'currency', messages)
        amt_exists = check_fare_amount(fare_transfer_rules_path, line, 'amount', 'currency', messages)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            messages.add_error(CURRENCY_WITHOUT_AMOUNT, line.line_num_error_msg, 'fare_transfer_rules.txt')

        check_amts(fare_transfer_rules_path, line, min_amt_exists, max_amt_exists, amt_exists, messages)

        if (min_amt_exists or max_amt_exists or amt_exists) and not line.fare_transfer_type:
            messages.add_error(AMOUNT_WITHOUT_FARE_TRANSFER_TYPE, line.line_num_error_msg)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.fare_transfer_type:
            messages.add_error(FARE_TRANSFER_TYPE_WITHOUT_AMOUNT, line.line_num_error_msg)
        if line.fare_transfer_type and (line.fare_transfer_type not in {'0', '1', '2', '3'}):
            messages.add_error(INVALID_FARE_TRANSFER_TYPE, line.line_num_error_msg)

        check_linked_flr_ftr_entities(fare_transfer_rules_path, line, rider_categories,
                                      rider_category_by_fare_container, linked_entities_by_fare_product, messages)

    if len(unused_leg_groups):
        warning_info = 'Unused leg groups: ' + str(unused_leg_groups)
        messages.add_warning(UNUSED_LEG_GROUPS, '', '', warning_info)
