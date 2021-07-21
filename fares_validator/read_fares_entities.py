# Reads files introduced as part of the GTFS fares-v2 specification

import re

from . import schema, diagnostics
from .errors import *
from .fare_leg_rule_checkers import check_areas, check_distances
from .fare_product_checkers import check_linked_fp_entities, check_bundle, check_durations_and_offsets
from .fare_transfer_rule_checkers import check_leg_groups, check_spans_and_transfer_ids, check_durations
from .utils import check_fare_amount, read_csv_file, check_linked_id, check_amts, check_linked_flr_ftr_entities
from .warnings import *


def areas(gtfs_root_dir, messages):
    greater_area_id_by_area_id = {}

    for line in read_csv_file(gtfs_root_dir, schema.AREAS, messages):
        if line.area_id in greater_area_id_by_area_id:
            line.add_error(DUPLICATE_AREA_ID)
            continue

        if not line.area_id:
            line.add_error(EMPTY_AREA_ID)
            continue

        greater_area_id_by_area_id[line.area_id] = line.greater_area_id

    for area_id in greater_area_id_by_area_id:
        greater_area_id = greater_area_id_by_area_id[area_id]

        while greater_area_id:
            if greater_area_id == area_id:
                messages.add_error(diagnostics.format(GREATER_AREA_ID_LOOP, '', '', f'area_id:  {area_id}'))
                break

            if greater_area_id not in greater_area_id_by_area_id:
                messages.add_error(diagnostics.format(UNDEFINED_GREATER_AREA_ID, '', '',
                                                      f'greater_area_id: {greater_area_id}'))
                break

            greater_area_id = greater_area_id_by_area_id[greater_area_id]

    return set(greater_area_id_by_area_id.keys())


def timeframes(gtfs_root_dir, messages):
    timeframes = set()
    for line in read_csv_file(gtfs_root_dir, schema.TIMEFRAMES,
                              messages):
        if not line.timeframe_id:
            line.add_error(EMPTY_TIMEFRAME_ID)
            continue
        if not line.start_time:
            line.add_error(EMPTY_START_TIME)
            continue
        if not line.end_time:
            line.add_error(EMPTY_END_TIME)
            continue

        starttimematch = re.search(r'^\d?\d:\d\d:\d\d$', line.start_time)
        endtimematch = re.search(r'^\d?\d:\d\d:\d\d$', line.end_time)

        if not starttimematch or not endtimematch:
            messages.add_error(INVALID_TIME_FORMAT, line.line_num_error_msg)
            timeframes.add(line.timeframe_id)
            continue

        starttime_split = line.start_time.split(':')
        endtime_split = line.end_time.split(':')

        if int(starttime_split[0]) > 23 or int(endtime_split[0]) > 23:
            line.add_error(INVALID_TIME_FORMAT)

        if int(starttime_split[1]) > 59 or int(endtime_split[1]) > 59:
            line.add_error(INVALID_TIME_FORMAT)

        if int(starttime_split[2]) > 59 or int(endtime_split[2]) > 59:
            line.add_error(INVALID_TIME_FORMAT)

        timeframes.add(line.timeframe_id)

    return timeframes


def rider_categories(gtfs_root_dir, messages):
    rider_categories = set()
    for line in read_csv_file(gtfs_root_dir,
                              schema.RIDER_CATEGORIES, messages):
        min_age_int = 0
        if not line.rider_category_id:
            line.add_error(EMPTY_RIDER_CATEGORY_ID)
            continue

        rider_categories.add(line.rider_category_id)

        if line.min_age:
            try:
                min_age_int = int(line.min_age)
                if min_age_int < 0:
                    line.add_error(NEGATIVE_MIN_AGE)
                if min_age_int > 100:
                    line.add_warning(VERY_LARGE_MIN_AGE)
            except ValueError:
                line.add_error(NON_INT_MIN_AGE)

        if line.max_age:
            try:
                max_age_int = int(line.max_age)
                if max_age_int < 0:
                    line.add_error(NEGATIVE_MAX_AGE)
                if max_age_int > 100:
                    line.add_warning(VERY_LARGE_MAX_AGE)
                if max_age_int <= min_age_int:
                    line.add_warning(MAX_AGE_LESS_THAN_MIN_AGE)
            except ValueError:
                line.add_error(NON_INT_MAX_AGE)

    return rider_categories


def fare_containers(gtfs_root_dir, rider_categories, messages):
    rider_category_by_fare_container = {}

    for line in read_csv_file(gtfs_root_dir,
                              schema.FARE_CONTAINERS, messages):
        if not line.fare_container_id:
            line.add_error(EMPTY_FARE_CONTAINER_ID)
            continue

        if not line.fare_container_name:
            line.add_error(EMPTY_FARE_CONTAINER_NAME)
            continue

        amount_exists = check_fare_amount(line, 'amount', 'currency')
        min_purchase_exists = check_fare_amount(line, 'minimum_initial_purchase', 'currency')
        if (not amount_exists and not min_purchase_exists) and line.currency:
            line.add_error(CURRENCY_WITHOUT_AMOUNT)

        if line.fare_container_id in rider_category_by_fare_container:
            line.add_error(DUPLICATE_FARE_CONTAINER_ID)
            continue

        if line.rider_category_id:
            if line.rider_category_id not in rider_categories:
                line.add_error(NONEXISTENT_RIDER_CATEGORY_ID)

        rider_category_by_fare_container[line.fare_container_id] = line.rider_category_id

    return rider_category_by_fare_container


def fare_products(gtfs_root_dir, gtfs, unused_timeframes, messages):
    linked_entities_by_fare_product = {}

    fare_products_path = gtfs_root_dir / 'fare_products.txt'

    for line in read_csv_file(gtfs_root_dir, schema.FARE_PRODUCTS, messages):
        if not line.fare_product_id:
            line.add_error(EMPTY_FARE_PRODUCT_ID)
            continue
        if not line.fare_product_name:
            line.add_error(EMPTY_FARE_PRODUCT_NAME)
            continue

        check_linked_fp_entities(line, gtfs.rider_category_ids, gtfs.rider_category_by_fare_container,
                                 linked_entities_by_fare_product)

        min_amt_exists = check_fare_amount(line, 'min_amount', 'currency')
        max_amt_exists = check_fare_amount(line, 'max_amount', 'currency')
        amt_exists = check_fare_amount(line, 'amount', 'currency')
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            line.add_error(CURRENCY_WITHOUT_AMOUNT)

        check_amts(fare_products_path, line, min_amt_exists, max_amt_exists, amt_exists)

        check_bundle(line)
        check_linked_id(line, 'service_id', gtfs.service_ids)
        timeframe_exists = check_linked_id(line, 'timeframe_id', gtfs.timeframe_ids)

        if line.timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.timeframe_id)
        if timeframe_exists:
            if line.timeframe_type not in {'0', '1'}:
                line.add_error(INVALID_TIMEFRAME_TYPE)
        else:
            if line.timeframe_type:
                line.add_error(TIMEFRAME_TYPE_WITHOUT_TIMEFRAME)

        check_durations_and_offsets(line)

    return linked_entities_by_fare_product


def fare_leg_rules(gtfs_root_dir, gtfs, unused_timeframes, messages):
    leg_group_ids = set()

    unused_areas = gtfs.areas.copy()
    unused_networks = gtfs.networks.copy()
    fare_leg_rules_path = gtfs_root_dir / 'fare_leg_rules.txt'

    if not fare_leg_rules_path.exists():
        messages.add_warning(diagnostics.format(NO_FARE_LEG_RULES, ''))

    for line in read_csv_file(gtfs_root_dir, schema.FARE_LEG_RULES, messages):
        if line.leg_group_id:
            leg_group_ids.add(line.leg_group_id)

        check_areas(line, gtfs.areas, unused_areas)

        check_linked_id(line, 'network_id', gtfs.networks)
        if line.network_id in unused_networks:
            unused_networks.remove(line.network_id)

        check_linked_id(line, 'from_timeframe_id', gtfs.timeframe_ids)
        if line.from_timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.from_timeframe_id)
        check_linked_id(line, 'to_timeframe_id', gtfs.timeframe_ids)
        if line.to_timeframe_id in unused_timeframes:
            unused_timeframes.remove(line.to_timeframe_id)

        check_linked_id(line, 'service_id', gtfs.service_ids)

        check_distances(line)

        min_amt_exists = check_fare_amount(line, 'min_amount', 'currency')
        max_amt_exists = check_fare_amount(line, 'max_amount', 'currency')
        amt_exists = check_fare_amount(line, 'amount', 'currency')
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            line.add_error(CURRENCY_WITHOUT_AMOUNT)
        check_amts(fare_leg_rules_path, line, min_amt_exists, max_amt_exists, amt_exists)
        if (min_amt_exists or max_amt_exists or amt_exists) and line.fare_product_id:
            line.add_error(AMOUNT_WITH_FARE_PRODUCT)

        if line.fare_leg_name and line.fare_product_id:
            line.add_error(FARE_LEG_NAME_WITH_FARE_PRODUCT)

        check_linked_flr_ftr_entities(line, gtfs.rider_category_ids, gtfs.rider_category_by_fare_container,
                                      gtfs.linked_entities_by_fare_product)

    if len(unused_areas):
        messages.add_warning(diagnostics.format(UNUSED_AREA_IDS, '', '', f'Unused areas: {unused_areas}'))

    if len(unused_networks):
        messages.add_warning(diagnostics.format(UNUSED_NETWORK_IDS, '', '', f'Unused networks: {unused_networks}'))

    return leg_group_ids


def fare_transfer_rules(gtfs_root_dir, gtfs, messages):
    unused_leg_groups = gtfs.leg_group_ids.copy()
    fare_transfer_rules_path = gtfs_root_dir / 'fare_transfer_rules.txt'

    if not fare_transfer_rules_path.exists():
        messages.add_warning(diagnostics.format(NO_FARE_TRANSFER_RULES, ''))

    for line in read_csv_file(gtfs_root_dir, schema.FARE_TRANSFER_RULES, messages):
        check_leg_groups(line, gtfs.leg_group_ids, unused_leg_groups)
        check_spans_and_transfer_ids(line)
        check_durations(line)

        min_amt_exists = check_fare_amount(line, 'min_amount', 'currency', )
        max_amt_exists = check_fare_amount(line, 'max_amount', 'currency')
        amt_exists = check_fare_amount(line, 'amount', 'currency')
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.currency:
            line.add_error(CURRENCY_WITHOUT_AMOUNT)

        check_amts(fare_transfer_rules_path, line, min_amt_exists, max_amt_exists, amt_exists)

        if (min_amt_exists or max_amt_exists or amt_exists) and not line.fare_transfer_type:
            line.add_error(AMOUNT_WITHOUT_FARE_TRANSFER_TYPE)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.fare_transfer_type:
            line.add_error(FARE_TRANSFER_TYPE_WITHOUT_AMOUNT)
        if line.fare_transfer_type and (line.fare_transfer_type not in {'0', '1', '2', '3'}):
            line.add_error(INVALID_FARE_TRANSFER_TYPE)

        check_linked_flr_ftr_entities(line, gtfs.rider_category_ids,
                                      gtfs.rider_category_by_fare_container, gtfs.linked_entities_by_fare_product)

    if len(unused_leg_groups):
        messages.add_warning(diagnostics.format(UNUSED_LEG_GROUPS, '', '',
                                                f'Unused leg groups: {unused_leg_groups}'))
