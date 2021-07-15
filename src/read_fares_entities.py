import re
from os import path

from .utils import check_fare_amount, read_csv_file, check_linked_id, check_amts, check_linked_flr_ftr_entities
from .fare_product_checkers import check_linked_fp_entities, check_bundle, check_durations_and_offsets
from .fare_leg_rule_checkers import check_areas, check_distances
from .fare_transfer_rule_checkers import check_leg_groups, check_spans_and_transfer_ids, check_durations

def timeframes(gtfs_root_dir, errors):
    timeframes = []
    def for_each_timeframe(line, line_num_error_msg):
        timeframe_id = line.get('timeframe_id')
        start_time = line.get('start_time')
        end_time = line.get('end_time')
        if not timeframe_id:
            errors.append('An entry in timeframes.txt contains an empty timeframe_id.' + line_num_error_msg)
            return
        if not start_time:
            errors.append('An entry in timeframes.txt contains an empty start_time.' + line_num_error_msg)
            return
        if not end_time:
            errors.append('An entry in timeframes.txt contains an empty end_time.' + line_num_error_msg)
            return

        starttimematch = re.search(r'^\d?\d:\d\d:\d\d$', start_time)
        endtimematch = re.search(r'^\d?\d:\d\d:\d\d$', end_time)

        invalid_time_string = 'A timeframe in timeframes.txt has an invalid time format, '
        invalid_time_string += 'timeframe_id: ' + timeframe_id + line_num_error_msg
        if not starttimematch or not endtimematch:
            errors.append(invalid_time_string)
            timeframes.append(timeframe_id)
            return

        starttime_split = start_time.split(':')
        endtime_split = end_time.split(':')
        
        if int(starttime_split[0]) > 23 or int(endtime_split[0]) > 23:
            errors.append(invalid_time_string)

        if int(starttime_split[1]) > 59 or int(endtime_split[1]) > 59:
            errors.append(invalid_time_string)

        if int(starttime_split[2]) > 59 or int(endtime_split[2]) > 59:
            errors.append(invalid_time_string)

        if timeframe_id in timeframes:
            # TODO: add check for overlapping timeframes on same id
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
            errors.append('A line in rider_categories.txt has an empty rider_category_id.' + line_num_error_msg)
            return

        if not rider_category in rider_categories:
            rider_categories.append(rider_category)
        
        if min_age:
            try:
                min_age_int = int(min_age)
                if min_age_int < 0:
                    errors.append('A line in rider_categories has a negative min_age.' + line_num_error_msg)
                if min_age_int > 100:
                    warnings.append('A line in rider_categories has a very large min_age.' + line_num_error_msg)
            except ValueError:
                errors.append('A line in rider_categories has a non-integer min_age.' + line_num_error_msg)
        if max_age:
            try:
                max_age_int = int(max_age)
                if max_age_int < 0:
                    errors.append('A line in rider_categories has a negative max_age.' + line_num_error_msg)
                if max_age_int > 100:
                    warnings.append('A line in rider_categories has a very large max_age.' + line_num_error_msg)
                if max_age_int <= min_age_int:
                    warnings.append('A line in rider_categories has max_age less than or equal to min_age.' + line_num_error_msg)
            except ValueError:
                errors.append('A line in rider_categories has a non-integer max_age.' + line_num_error_msg)

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
            errors.append('An entry in fare_containers.txt does not have a fare_container_id.' + line_num_error_msg)
            return

        if not fare_container_name:
            errors.append('An entry in fare_containers.txt does not have a fare_container_name.' + line_num_error_msg)
            return

        amount_exists = check_fare_amount(fare_containers_path, line, line_num_error_msg, 'amount', 'currency', errors)
        min_purchase_exists = check_fare_amount(fare_containers_path, line, line_num_error_msg, 'minimum_initial_purchase', 'currency', errors)
        if (not amount_exists and not min_purchase_exists) and line.get('currency'):
            errors.append('Fare_containers: A currency is defined without an amount to accompany it.' + line_num_error_msg)

        if fare_container_id in rider_category_by_fare_container:
            error_string = 'A fare container id is defined twice in fare_containers.txt: '
            error_string += fare_container_id + line_num_error_msg
            errors.append(error_string)
            return

        if rider_category_id:
            if not rider_category_id in rider_categories:
                error_string = 'A rider_category_id referenced in fare_containers.txt is not defined '
                error_string += 'in rider_categories.txt: '
                error_string += rider_category_id + line_num_error_msg
                errors.append(error_string)

        rider_category_by_fare_container[fare_container_id] = rider_category_id
    
    if not path.isfile(fare_containers_path):
        return rider_category_by_fare_container

    read_csv_file(fare_containers_path, ['fare_container_id', 'fare_container_name'], errors, for_each_fare_container)

    return rider_category_by_fare_container

def fare_products(gtfs_root_dir, dependent_entities, errors, warnings):
    linked_entities_by_fare_product = {}
    
    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']

    fare_products_path = path.join(gtfs_root_dir, 'fare_products.txt')

    def for_each_fare_product(line, line_num_error_msg):
        if not line.get('fare_product_id'):
            errors.append('An entry in fare_products.txt has an empty fare_product_id.' + line_num_error_msg)
            return
        if not line.get('fare_product_name'):
            errors.append('An entry in fare_products.txt has an empty fare_product_name.' + line_num_error_msg)
            return
        
        check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)

        min_amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_products_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            errors.append('Fare_products: A currency is defined without an amount to accompany it.' + line_num_error_msg)
        check_amts(fare_products_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)

        check_bundle(line, line_num_error_msg, errors)
        check_linked_id(path, line, 'service_id', service_ids, line_num_error_msg, errors)
        timeframe_exists = check_linked_id(path, line, 'timeframe_id', timeframe_ids, line_num_error_msg, errors)
        if timeframe_exists:
            if not line.get('timeframe_type') in ['0', '1']:
                error_string = 'A timeframe_type in fare_products.txt has an invalid value, or is required and does not exist.'
                error_string += line_num_error_msg
                errors.append(error_string)
        else:
            if line.get('timeframe_type'):
                error_string = 'A timeframe_type in fare_products.txt is referenced without an accompanying timeframe_id.'
                error_string += line_num_error_msg
                errors.append(error_string)
        
        check_durations_and_offsets(line, line_num_error_msg, errors, warnings)

    if not path.isfile(fare_products_path):
        return linked_entities_by_fare_product
    
    read_csv_file(fare_products_path, ['fare_product_id', 'fare_product_name'], errors, for_each_fare_product)

    return linked_entities_by_fare_product

def fare_leg_rules(gtfs_root_dir, dependent_entities, errors):
    leg_group_ids = []

    areas =  dependent_entities['areas']
    networks =  dependent_entities['networks']
    service_ids = dependent_entities['service_ids']
    timeframe_ids = dependent_entities['timeframe_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_leg_rules_path = path.join(gtfs_root_dir, 'fare_leg_rules.txt')

    def for_each_fare_leg_rule(line, line_num_error_msg):
        if line.get('leg_group_id') and not line.get('leg_group_id') in leg_group_ids:
            leg_group_ids.append(line.get('leg_group_id'))

        check_areas(fare_leg_rules_path, line, line_num_error_msg, areas, errors)
        check_linked_id(fare_leg_rules_path, line, 'network_id', networks, line_num_error_msg, errors)
        check_linked_id(fare_leg_rules_path, line, 'from_timeframe_id', timeframe_ids, line_num_error_msg, errors)
        check_linked_id(fare_leg_rules_path, line, 'to_timeframe_id', timeframe_ids, line_num_error_msg, errors)
        check_linked_id(fare_leg_rules_path, line, 'service_id', service_ids, line_num_error_msg, errors)
        check_distances(line, line_num_error_msg, errors)

        min_amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_leg_rules_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            errors.append('Fare_leg_rules: A currency is defined without an amount to accompany it.' + line_num_error_msg)
        check_amts(fare_leg_rules_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)
        if (min_amt_exists or max_amt_exists or amt_exists) and line.get('fare_product_id'):
            errors.append('An entry in fare_leg_rules has both a fare_product and an amount field defined.' + line_num_error_msg)
        
        if line.get('fare_leg_name') and line.get('fare_product_id'):
            errors.append('An entry in fare_leg_rules has both a fare_product and a fare_leg_name defined.' + line_num_error_msg)
        
        check_linked_flr_ftr_entities(fare_leg_rules_path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)
        
    if not path.isfile(fare_leg_rules_path):
        return leg_group_ids
    
    read_csv_file(fare_leg_rules_path, [], errors, for_each_fare_leg_rule)

    return leg_group_ids

def fare_transfer_rules(gtfs_root_dir, dependent_entities, errors):
    leg_group_ids = dependent_entities['leg_group_ids']
    rider_categories = dependent_entities['rider_category_ids']
    rider_category_by_fare_container = dependent_entities['rider_category_by_fare_container']
    linked_entities_by_fare_product = dependent_entities['linked_entities_by_fare_product']

    fare_transfer_rules_path = path.join(gtfs_root_dir, 'fare_transfer_rules.txt')

    def for_each_fare_transfer_rule(line, line_num_error_msg):
        check_leg_groups(line, line_num_error_msg, leg_group_ids, errors)
        check_spans_and_transfer_ids(line, line_num_error_msg, errors)
        check_durations(line, line_num_error_msg, errors)

        min_amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'min_amount', 'currency', errors)
        max_amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'max_amount', 'currency', errors)
        amt_exists = check_fare_amount(fare_transfer_rules_path, line, line_num_error_msg, 'amount', 'currency', errors)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('currency'):
            errors.append('Fare_leg_rules: A currency is defined without an amount to accompany it.' + line_num_error_msg)
        check_amts(fare_transfer_rules_path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors)

        if (min_amt_exists or max_amt_exists or amt_exists) and not line.get('fare_transfer_type'):
            errors.append('A fare_transfer_rule has an amount field defined without fare_transfer_type.' + line_num_error_msg)
        if (not min_amt_exists and not max_amt_exists and not amt_exists) and line.get('fare_transfer_type'):
            errors.append('A fare_transfer_rule has fare_transfer_type defined without an amount field.' + line_num_error_msg)
        if line.get('fare_transfer_type') and (line.get('fare_transfer_type') not in ['0', '1', '2', '3']):
            errors.append('A fare_transfer_rule has fare_transfer_type with invalid value.' + line_num_error_msg)
        
        check_linked_flr_ftr_entities(fare_transfer_rules_path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors)
    
    if not path.isfile(fare_transfer_rules_path):
        return
    
    read_csv_file(fare_transfer_rules_path, [], errors, for_each_fare_transfer_rule)