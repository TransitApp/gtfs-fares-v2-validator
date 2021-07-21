import csv
from .decimals_by_currency import decimals_by_currency
from .errors import *
from .warnings import *
from pathlib import Path


class Entity:
    def __init__(self, original_dict):
        self.data = original_dict

    def __getattr__(self, item):
        return self.data.get(item)


def read_csv_file(path, required_fields, expected_fields, messages, func):
    filename = Path(path).name
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for required_field in required_fields:
            if required_field not in reader.fieldnames:
                extra_info = 'field: ' + required_field
                messages.add_error(REQUIRED_FIELD_MISSING, '', filename, extra_info)
                return False

        if len(expected_fields):
            unexpected_fields = []
            for field in reader.fieldnames:
                if field not in expected_fields:
                    unexpected_fields.append(field)
            if len(unexpected_fields):
                extra_info = '\nColumn(s): ' + str(unexpected_fields)
                messages.add_warning(UNEXPECTED_FIELDS, '', filename, extra_info)

        for line in reader:
            entity = Entity(line)
            line_num_error_msg = '\nLine: ' + str(reader.line_num)
            func(entity, line_num_error_msg)

def check_fare_amount(path, line, line_num_error_msg, fare_field, currency_field, messages):
    filename = Path(path).name
    fare = getattr(line, fare_field)
    currency = getattr(line, currency_field)

    if fare:
        if not currency:
            messages.add_error(AMOUNT_WITHOUT_CURRENCY, line_num_error_msg, filename)
            return True
        if currency not in decimals_by_currency:
            messages.add_error(UNRECOGNIZED_CURRENCY_CODE, line_num_error_msg, filename)
            return True
        try:
            float(fare)
            if '.' in fare:
                num_decimal_points = len(fare.split('.')[1])
                if num_decimal_points > decimals_by_currency[currency]:
                    messages.add_error(TOO_MANY_AMOUNT_DECIMALS, line_num_error_msg, filename)
        except Exception:
            messages.add_error(INVALID_AMOUNT_FORMAT, line_num_error_msg, filename)
        return True
    else:
        return False

def check_amts(path, line_num_error_msg, min_amt_exists, max_amt_exists, amt_exists, messages):
    filename = Path(path).name
    if (min_amt_exists or max_amt_exists) and amt_exists:
        messages.add_error(AMOUNT_WITH_MIN_OR_MAX_AMOUNT, line_num_error_msg, filename)
    if (min_amt_exists and not max_amt_exists) or (max_amt_exists and not min_amt_exists):
        messages.add_error(MISSING_MIN_OR_MAX_AMOUNT, line_num_error_msg, filename)
    if (not amt_exists and not min_amt_exists and not max_amt_exists) and filename == 'fare_products.txt':
        messages.add_error(NO_AMOUNT_DEFINED, line_num_error_msg)

def check_areas_of_file(path, stop_or_stop_time, areas, unused_areas, messages):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        if 'area_id' in reader.fieldnames:
            for line in reader:
                area_id = line.get('area_id')

                if not area_id:
                    continue

                if area_id not in areas:
                    line_num_error_msg = '\nLine: ' + str(reader.line_num)
                    messages.add_error(NONEXISTENT_AREA_ID, line_num_error_msg, stop_or_stop_time)
                    continue

                if area_id in unused_areas:
                    unused_areas.remove(area_id)

def check_linked_id(path, line, fieldname, defined_ids, line_num_error_msg, messages):
    filename = Path(path).name
    if not getattr(line, fieldname):
        return False
    
    if getattr(line, fieldname) not in defined_ids:
        error_info = fieldname + ': ' + getattr(line, fieldname)
        messages.add_error(FOREIGN_ID_INVALID, line_num_error_msg, filename, error_info)

    return True

def check_linked_flr_ftr_entities(path, line, line_num_error_msg, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product, messages):
    filename = Path(path).name

    if line.fare_product_id and line.fare_product_id not in linked_entities_by_fare_product:
        messages.add_error(NONEXISTENT_FARE_PRODUCT_ID, line_num_error_msg, filename)
    if line.rider_category_id and line.rider_category_id not in rider_categories:
        messages.add_error(NONEXISTENT_RIDER_CATEGORY_ID, line_num_error_msg, filename)
    if line.fare_container_id and line.fare_container_id not in rider_category_by_fare_container:
        messages.add_error(NONEXISTENT_FARE_CONTAINER_ID, line_num_error_msg, filename)
    
    if line.fare_product_id:
        if line.rider_category_id:
            fp_rider_cats = linked_entities_by_fare_product[line.fare_product_id].get('rider_category_ids')
            if len(fp_rider_cats) and (line.rider_category_id not in fp_rider_cats):
                messages.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_PRODUCT, line_num_error_msg, filename)
        if line.fare_container_id:
            fp_fare_containers = linked_entities_by_fare_product[line.fare_product_id].get('fare_container_ids')
            if len(fp_fare_containers) and (line.fare_container_id not in fp_fare_containers):
                messages.add_error(CONFLICTING_FARE_CONTAINER_ON_FARE_PRODUCT, line_num_error_msg, filename)
    if line.rider_category_id and line.fare_container_id:
        fc_rider_cat = rider_category_by_fare_container[line.fare_container_id]
        if fc_rider_cat and (fc_rider_cat != line.rider_category_id):
            messages.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER, line_num_error_msg, filename)
