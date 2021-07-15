import csv

def get_filename_of_path(path):
    path_split = path.split('/')
    file = path_split[len(path_split) - 1]
    return file.split('.')[0]

def read_csv_file(path, required_fields, errors, func):
    filename = get_filename_of_path(path)
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for required_field in required_fields:
            if not required_field in reader.fieldnames:
                errors.append(filename + ' is missing required field ' + required_field)
                return False
        
        for line in reader:
            line_num_error_msg = '\nLine: ' + str(reader.line_num)
            func(line, line_num_error_msg)

def check_fare_amount(path, line, line_num_error_msg, fare_field, currency_field, errors):
    filename = get_filename_of_path(path)
    fare, currency = '', ''

    fare = line.get(fare_field)
    currency = line.get(currency_field)

    if fare:
        if not currency:
            error_string = filename + ': A fare or other monetary amount has been defined without a currency.'
            error_string += line_num_error_msg
            errors.append(error_string)
            return True
        try:
            float(fare)
        except Exception:
            error_string = filename + ': A fare field was defined, but is not an integer or float.'
            error_string += line_num_error_msg
            errors.append(error_string)
        # TODO: create a list of acceptable currency codes.
        return True
    else:
        return False

def check_amts(path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, errors):
    filename = get_filename_of_path(path)
    if (min_amt_exists or max_amt_exists) and amt_exists:
        error_string = filename + ': An entry has amount and at least one of min_ or max_amount defined.'
        error_string += line_num_error_msg
        errors.append(error_string)
    if (min_amt_exists and not max_amt_exists) or (max_amt_exists and not min_amt_exists):
        error_string = filename + ': An entry has a min_ or max_amount defined without its counterpart.'
        error_string += line_num_error_msg
        errors.append(error_string)
    if (not amt_exists and not min_amt_exists and not max_amt_exists) and filename == 'fare_products':
        error_string = filename + ': An entry has no amount, min_amount, or max_amount.'
        error_string += line_num_error_msg
        errors.append(error_string)

def check_areas_of_file(path, stop_or_stop_time, areas, unused_areas, errors):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        if 'area_id' in reader.fieldnames:
            for line in reader:
                area_id = line.get('area_id')

                if not area_id:
                    continue

                if not area_id in areas:
                    error_string = 'A ' + stop_or_stop_time + ' in ' + stop_or_stop_time + 's.txt'
                    error_string += ' references an area_id that does not exist: '
                    error_string += ' area_id: ' + area_id
                    error_string += '\nLine: ' + str(reader.line_num)
                    errors.append(error_string)
                    continue

                if area_id in unused_areas:
                    unused_areas.remove(area_id)

def check_linked_id(path, line, fieldname, defined_ids, line_num_error_msg, errors):
    filename = get_filename_of_path(path)
    if not line.get(fieldname):
        return False
    
    if not line.get(fieldname) in defined_ids:
        error_string = filename + ': A ' + fieldname + ' is referenced, but it does not exist.'
        error_string += line_num_error_msg
        errors.append(error_string)

    return True

def check_linked_flr_ftr_entities(path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, errors):
    filename = get_filename_of_path(path)
    fare_product_id = line.get('fare_product_id')
    rider_category_id = line.get('rider_category_id')
    fare_container_id = line.get('fare_container_id')

    if fare_product_id and not fare_product_id in linked_entities_by_fare_product:
        errors.append(filename + ': An entry references a fare product that does not exist.' + line_num_error_msg)
    if rider_category_id and not rider_category_id in rider_categories:
        errors.append(filename + ': An entry references a rider category that does not exist.' + line_num_error_msg)
    if fare_container_id and not fare_container_id in rider_category_by_fare_container:
        errors.append(filename + ': An entry references a fare container that does not exist.' + line_num_error_msg)
    
    if fare_product_id:
        if rider_category_id:
            fp_rider_cat = linked_entities_by_fare_product[fare_product_id].get('rider_category_id')
            if fp_rider_cat and (not fp_rider_cat == rider_category_id):
                error_string = filename + ': An entry has a conflicting rider_category_id '
                error_string += ' and fare_product.rider_category_id.' + line_num_error_msg
                errors.push(error_string)
        if fare_container_id:
            fp_fare_container = linked_entities_by_fare_product[fare_product_id].get('fare_container_id')
            if fp_fare_container and (not fp_fare_container == fare_container_id):
                error_string = filename + ': An entry has a conflicting fare_container_id '
                error_string += ' and fare_product.fare_container_id.' + line_num_error_msg
                errors.push(error_string)
    else:
        if rider_category_id and fare_container_id:
            fc_rider_cat = rider_category_by_fare_container[fare_container_id]
            if fc_rider_cat and (not fc_rider_cat == rider_category_id):
                error_string = filename + ': An entry has a conflicting rider_category_id '
                error_string += ' and fare_container.rider_category_id.' + line_num_error_msg
                errors.push(error_string)