def check_linked_fp_entities(line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors):
    rider_category_id = line.get('rider_category_id')
    fare_container_id = line.get('fare_container_id')
    linked_entities = {}

    if rider_category_id:
        linked_entities['rider_category_id'] = rider_category_id
        if (not rider_category_id in rider_categories):
            error_string = 'An entry in fare_products.txt references a non-existent rider category.'
            error_string += '\nrider_category_id: ' + rider_category_id
            error_string += '\nfare_product_id: ' + line['fare_product_id']
            error_string += line_num_error_msg
            errors.append(error_string)
    
    if fare_container_id:
        linked_entities['fare_container_id'] = fare_container_id
        if not fare_container_id in rider_category_by_fare_container:
            error_string = 'An entry in fare_products.txt references a non-existent fare container.'
            error_string += '\nfare_container_id: ' + fare_container_id
            error_string += '\nfare_product_id: ' + line['fare_product_id']
            error_string += line_num_error_msg
            errors.append(error_string)
        fare_container_rider_cat = rider_category_by_fare_container[fare_container_id]
        if rider_category_id and fare_container_rider_cat and (rider_category_id != fare_container_rider_cat):
            error_string = 'An entry in fare_products.txt references a conflicting rider_category_id and fare container.'
            error_string += '\nfare_container_id: ' + fare_container_id
            error_string += '\nrider_category_id: ' + rider_category_id
            error_string += '\nfare_product_id: ' + line['fare_product_id']
            error_string += line_num_error_msg
            errors.append(error_string)
    
    linked_entities_by_fare_product[line['fare_product_id']] = linked_entities

def check_bundle(line, line_num_error_msg, errors):
    if line.get('bundle_amount'):
        error_string = 'A bundle amount in fare_products.txt has an invalid value.' 
        error_string += line_num_error_msg
        try:
            bundle_amt = int(line.get('bundle_amount'))
            if bundle_amt < 0:
                errors.append(error_string)
        except ValueError:
            errors.append(error_string)

def check_durations_and_offsets(line, line_num_error_msg, errors, warnings):
    duration_start = line.get('duration_start')
    if duration_start and (duration_start not in ['0', '1']):
        errors.append('A duration_start in fare_products.txt is not one of the accepted values.' + line_num_error_msg)
    
    duration_unit = line.get('duration_unit')
    if duration_unit and (not duration_unit in ['0', '1', '2', '3', '4', '5', '6']):
        errors.append('A duration_unit in fare_products.txt is not one of the accepted values.' + line_num_error_msg)
    
    duration_type = line.get('duration_type')
    if duration_type and (not duration_type in ['1', '2']):
        errors.append('A duration_unit in fare_products.txt is not one of the accepted values.' + line_num_error_msg)
    
    if duration_type == '1' and duration_start:
        errors.append('A duration_start in fare_products.txt is defined with duration_type=1.' + line_num_error_msg)

    duration_amount = line.get('duration_amount')
    if duration_amount:
        try:
            amt = int(duration_amount)
            if amt < 1:
                errors.append('A duration amount in fare_products.txt is 0 or negative.' + line_num_error_msg)
        except ValueError:
            errors.append('A duration amount in fare_products.txt is not an integer.' + line_num_error_msg)
        
        if not duration_unit:
            errors.append('A duration amount in fare_products.txt is defined without duration_unit.' + line_num_error_msg)

        if not duration_type:
            errors.append('A duration amount in fare_products.txt is defined without duration_type.' + line_num_error_msg)
    else:
        if duration_type:
            errors.append('A duration type in fare_products.txt is defined without duration_amount.' + line_num_error_msg)
        if duration_unit:
            errors.append('A duration unit in fare_products.txt is defined without duration_amount.' + line_num_error_msg)

    offset_unit = line.get('offset_unit')
    if offset_unit and (not offset_unit in ['0', '1', '2', '3', '4', '5', '6']):
        errors.append('An offset_unit in fare_products.txt is not one of the accepted values.' + line_num_error_msg)

    offset_amt = line.get('offset_amount')
    if offset_amt:
        try:
            amt = int(offset_amt)
        except ValueError:
            errors.append('A offset amount in fare_products.txt is not an integer.' + line_num_error_msg)
        
        if duration_type == '2':
            errors.append('A offset amount in fare_products.txt is defined for duration_type=2.' + line_num_error_msg)
        
        if not offset_unit:
            warnings.append('A offset amount in fare_products.txt is defined without an offset unit, so duration_unit will be used.' + line_num_error_msg)
    else:
        if offset_unit:
            errors.append('A offset unit in fare_products.txt is defined without an offset amount.' + line_num_error_msg)
