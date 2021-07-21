from .errors import *
from .warnings import *

def check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, messages):
    fare_product_id = line.get('fare_product_id')
    rider_category_id = line.get('rider_category_id')
    fare_container_id = line.get('fare_container_id')
    linked_entities = linked_entities_by_fare_product.get(fare_product_id)
    if not linked_entities:
        linked_entities = {
            'rider_category_ids': [],
            'fare_container_ids': [],
        }

    if rider_category_id:
        linked_entities['rider_category_ids'].append(rider_category_id)
        if rider_category_id not in rider_categories:
            messages.add_error(NONEXISTENT_RIDER_CATEGORY_ID, line_num_error_msg)
    
    if fare_container_id:
        linked_entities['fare_container_ids'].append(fare_container_id)
        if fare_container_id not in rider_category_by_fare_container:
            messages.add_error(NONEXISTENT_FARE_CONTAINER_ID, line_num_error_msg, 'fare_products.txt')

        fare_container_rider_cat = rider_category_by_fare_container.get(fare_container_id)
        if rider_category_id and fare_container_rider_cat and (rider_category_id != fare_container_rider_cat):
            messages.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER, line_num_error_msg, 'fare_products.txt')
    
    linked_entities_by_fare_product[fare_product_id] = linked_entities

def check_bundle(line, line_num_error_msg, messages):
    if line.get('bundle_amount'):
        try:
            bundle_amt = int(line.get('bundle_amount'))
            if bundle_amt < 0:
                messages.add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg)
        except ValueError:
            messafes.add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg)

def check_durations_and_offsets(line, line_num_error_msg, messages):
    duration_start = line.get('duration_start')
    if duration_start and duration_start not in {'0', '1'}:
        messages.add_error(INVALID_DURATION_START, line_num_error_msg)
    
    duration_unit = line.get('duration_unit')
    if duration_unit and duration_unit in {'0', '1', '2', '3', '4', '5', '6'}:
        messages.add_error(INVALID_DURATION_UNIT, line_num_error_msg)
    
    duration_type = line.get('duration_type')
    if duration_type and duration_type in {'1', '2'}:
        messages.add_error(INVALID_DURATION_TYPE, line_num_error_msg)
    
    if duration_type == '1' and duration_start:
        messages.add_error(DURATION_START_WITH_DURATION_TYPE, line_num_error_msg)

    duration_amount = line.get('duration_amount')
    if duration_amount:
        try:
            amt = int(duration_amount)
            if amt < 1:
                messages.add_error(NEGATIVE_OR_ZERO_DURATION, line_num_error_msg)
        except ValueError:
            messages.add_error(NON_INT_DURATION_AMOUNT, line_num_error_msg)
        
        if not duration_unit:
            messages.add_error(DURATION_WITHOUT_UNIT, line_num_error_msg)

        if not duration_type:
            messages.add_error(DURATION_WITHOUT_TYPE, line_num_error_msg)
    else:
        if duration_type:
            messages.add_error(DURATION_TYPE_WITHOUT_AMOUNT, line_num_error_msg)
        if duration_unit:
            messages.add_error(DURATION_UNIT_WITHOUT_AMOUNT, line_num_error_msg)

    offset_unit = line.get('offset_unit')
    if offset_unit and offset_unit not in {'0', '1', '2', '3', '4', '5', '6'}:
        messages.add_error(INVALID_OFFSET_UNIT, line_num_error_msg)

    offset_amt = line.get('offset_amount')
    if offset_amt:
        try:
            amt = int(offset_amt)
        except ValueError:
            messages.add_error(NON_INT_OFFSET_AMOUNT, line_num_error_msg)
        
        if duration_type == '2':
            messages.add_error(OFFSET_AMOUNT_WITH_DURATION_TYPE, line_num_error_msg)
        
        if not offset_unit:
            messages.add_warning(OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT, line_num_error_msg)
    else:
        if offset_unit:
            messages.add_error(OFFSET_UNIT_WITHOUT_AMOUNT, line_num_error_msg)
