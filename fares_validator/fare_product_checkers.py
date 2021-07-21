from .errors import *
from .warnings import *

def check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, messages):
    linked_entities = linked_entities_by_fare_product.get(line.fare_product_id)
    if not linked_entities:
        linked_entities = {
            'rider_category_ids': [],
            'fare_container_ids': [],
        }

    if line.rider_category_id:
        linked_entities['rider_category_ids'].append(line.rider_category_id)
        if line.rider_category_id not in rider_categories:
            messages.add_error(NONEXISTENT_RIDER_CATEGORY_ID, line_num_error_msg)
    
    if line.fare_container_id:
        linked_entities['fare_container_ids'].append(line.fare_container_id)
        if line.fare_container_id not in rider_category_by_fare_container:
            messages.add_error(NONEXISTENT_FARE_CONTAINER_ID, line_num_error_msg, 'fare_products.txt')

        fare_container_rider_cat = rider_category_by_fare_container.get(line.fare_container_id)
        if line.rider_category_id and fare_container_rider_cat and (line.rider_category_id != fare_container_rider_cat):
            messages.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER, line_num_error_msg, 'fare_products.txt')
    
    linked_entities_by_fare_product[line.fare_product_id] = linked_entities

def check_bundle(line, line_num_error_msg, messages):
    if line.bundle_amount:
        try:
            bundle_amt = int(line.bundle_amount)
            if bundle_amt < 0:
                messages.add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_BUNDLE_AMOUNT, line_num_error_msg)

def check_durations_and_offsets(line, line_num_error_msg, messages):
    if line.duration_start and line.duration_start not in {'0', '1'}:
        messages.add_error(INVALID_DURATION_START, line_num_error_msg)

    if line.duration_unit and line.duration_unit not in {'0', '1', '2', '3', '4', '5', '6'}:
        messages.add_error(INVALID_DURATION_UNIT, line_num_error_msg)

    if line.duration_type and line.duration_type in {'1', '2'}:
        messages.add_error(INVALID_DURATION_TYPE, line_num_error_msg)
    
    if line.duration_type == '1' and line.duration_start:
        messages.add_error(DURATION_START_WITH_DURATION_TYPE, line_num_error_msg)

    if line.duration_amount:
        try:
            amt = int(line.duration_amount)
            if amt < 1:
                messages.add_error(NEGATIVE_OR_ZERO_DURATION, line_num_error_msg)
        except ValueError:
            messages.add_error(NON_INT_DURATION_AMOUNT, line_num_error_msg)
        
        if not line.duration_unit:
            messages.add_error(DURATION_WITHOUT_UNIT, line_num_error_msg)

        if not line.duration_type:
            messages.add_error(DURATION_WITHOUT_TYPE, line_num_error_msg)
    else:
        if line.duration_type:
            messages.add_error(DURATION_TYPE_WITHOUT_AMOUNT, line_num_error_msg)
        if line.duration_unit:
            messages.add_error(DURATION_UNIT_WITHOUT_AMOUNT, line_num_error_msg)

    if line.offset_unit and line.offset_unit not in {'0', '1', '2', '3', '4', '5', '6'}:
        messages.add_error(INVALID_OFFSET_UNIT, line_num_error_msg)

    if line.offset_amount:
        try:
            amt = int(line.offset_amount)
        except ValueError:
            messages.add_error(NON_INT_OFFSET_AMOUNT, line_num_error_msg)
        
        if line.duration_type == '2':
            messages.add_error(OFFSET_AMOUNT_WITH_DURATION_TYPE, line_num_error_msg)
        
        if not line.offset_unit:
            messages.add_warning(OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT, line_num_error_msg)
    else:
        if line.offset_unit:
            messages.add_error(OFFSET_UNIT_WITHOUT_AMOUNT, line_num_error_msg)
