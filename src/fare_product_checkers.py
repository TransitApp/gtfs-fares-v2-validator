from .errors import *

def check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors):
    rider_category_id = line.get('rider_category_id')
    fare_container_id = line.get('fare_container_id')
    linked_entities = {}

    if rider_category_id:
        linked_entities['rider_category_id'] = rider_category_id
        if (not rider_category_id in rider_categories):
            add_error(NONEXISTENT_RIDER_CATEGORY_ID, line_num_error_msg, errors)
    
    if fare_container_id:
        linked_entities['fare_container_id'] = fare_container_id
        if not fare_container_id in rider_category_by_fare_container:
            add_error(NONEXISTENT_FARE_CONTAINER_ID, line_num_error_msg, errors, 'fare_products.txt')

        fare_container_rider_cat = rider_category_by_fare_container.get(fare_container_id)
        if rider_category_id and fare_container_rider_cat and (rider_category_id != fare_container_rider_cat):
            add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER, line_num_error_msg, errors, 'fare_products.txt')
    
    linked_entities_by_fare_product[line['fare_product_id']] = linked_entities

def check_bundle(line, line_num_error_msg, errors):
    if line.get('bundle_amount'):
        try:
            bundle_amt = int(line.get('bundle_amount'))
            if bundle_amt < 0:
                add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg, errors)
        except ValueError:
            add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg, errors)

def check_durations_and_offsets(line, line_num_error_msg, errors, warnings):
    duration_start = line.get('duration_start')
    if duration_start and (duration_start not in ['0', '1']):
        add_error(INVALID_DURATION_START, line_num_error_msg, errors)
    
    duration_unit = line.get('duration_unit')
    if duration_unit and (not duration_unit in ['0', '1', '2', '3', '4', '5', '6']):
        add_error(INVALID_DURATION_UNIT, line_num_error_msg, errors)
    
    duration_type = line.get('duration_type')
    if duration_type and (not duration_type in ['1', '2']):
        add_error(INVALID_DURATION_TYPE, line_num_error_msg, errors)
    
    if duration_type == '1' and duration_start:
        add_error(DURATION_START_WITH_DURATION_TYPE, line_num_error_msg, errors)

    duration_amount = line.get('duration_amount')
    if duration_amount:
        try:
            amt = int(duration_amount)
            if amt < 1:
                add_error(NEGATIVE_OR_ZERO_DURATION, line_num_error_msg, errors)
        except ValueError:
            add_error(NON_INT_DURATION_AMOUNT, line_num_error_msg, errors)
        
        if not duration_unit:
            add_error(DURATION_WITHOUT_UNIT, line_num_error_msg, errors)

        if not duration_type:
            add_error(DURATION_WITHOUT_TYPE, line_num_error_msg, errors)
    else:
        if duration_type:
            add_error(DURATION_TYPE_WITHOUT_AMOUNT, line_num_error_msg, errors)
        if duration_unit:
            add_error(DURATION_UNIT_WITHOUT_AMOUNT, line_num_error_msg, errors)

    offset_unit = line.get('offset_unit')
    if offset_unit and (not offset_unit in ['0', '1', '2', '3', '4', '5', '6']):
        add_error(INVALID_OFFSET_UNIT, line_num_error_msg, errors)

    offset_amt = line.get('offset_amount')
    if offset_amt:
        try:
            amt = int(offset_amt)
        except ValueError:
            add_error(NON_INT_OFFSET_AMOUNT, line_num_error_msg, errors)
        
        if duration_type == '2':
            add_error(OFFSET_AMOUNT_WITH_DURATION_TYPE, line_num_error_msg, errors)
        
        if not offset_unit:
            warnings.append('An offset_amount in fare_products.txt is defined without an offset_unit, so duration_unit will be used.' + line_num_error_msg)
    else:
        if offset_unit:
            add_error(OFFSET_UNIT_WITHOUT_AMOUNT, line_num_error_msg, errors)
