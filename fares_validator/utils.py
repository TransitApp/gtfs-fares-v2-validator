import csv
from pathlib import Path

from .decimals_by_currency import decimals_by_currency
from .errors import *
from .warnings import *
from . import diagnostics


class Entity:
    def __init__(self, entity_filename, messages, original_dict):
        self._entity_filename = entity_filename
        self._messages = messages
        self._data = original_dict

    def __getattr__(self, item):
        return self._data.get(item)

    def add_error(self, code, extra_info=''):
        self._messages.add_error(diagnostics.format(code, self.line_num_error_msg, self._entity_filename, extra_info))

    def add_warning(self, code, extra_info=''):
        self._messages.add_warning(diagnostics.format(code, self.line_num_error_msg, self._entity_filename, extra_info))


def read_csv_file(path, required_fields, defined_fields, messages, message_if_missing=None):
    path = Path(path)

    if not path.exists():
        if message_if_missing:
            messages.add_warning(diagnostics.format(message_if_missing))
        return

    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for required_field in required_fields:
            if required_field not in reader.fieldnames:
                messages.add_error(diagnostics.format(REQUIRED_FIELD_MISSING, '', path.name, f'field:  {required_field}'))
                return False

        if len(defined_fields):
            unexpected_fields = []
            for field in reader.fieldnames:
                if field not in defined_fields:
                    unexpected_fields.append(field)
            if len(unexpected_fields):
                messages.add_warning(diagnostics.format(UNEXPECTED_FIELDS, '', path.name,
                                                        f'\nColumn(s): {unexpected_fields}'))

        for line in reader:
            line['line_num_error_msg'] = f'\nLine: {reader.line_num}'
            entity = Entity(path.name, messages, line)
            yield entity


def check_fare_amount(line, fare_field, currency_field):
    fare = getattr(line, fare_field)
    currency = getattr(line, currency_field)

    if fare:
        if not currency:
            line.add_error(AMOUNT_WITHOUT_CURRENCY)
            return True
        if currency not in decimals_by_currency:
            line.add_error(UNRECOGNIZED_CURRENCY_CODE)
            return True
        try:
            float(fare)
            if '.' in fare:
                num_decimal_places = len(fare.split('.')[1])
                if num_decimal_places > decimals_by_currency[currency]:
                    line.add_error(TOO_MANY_AMOUNT_DECIMALS)
        except Exception:
            line.add_error(INVALID_AMOUNT_FORMAT)
        return True
    else:
        return False


def check_amts(path, line, min_amt_exists, max_amt_exists, amt_exists):
    filename = Path(path).name
    if (min_amt_exists or max_amt_exists) and amt_exists:
        line.add_error(AMOUNT_WITH_MIN_OR_MAX_AMOUNT)
    if (min_amt_exists and not max_amt_exists) or (max_amt_exists and not min_amt_exists):
        line.add_error(MISSING_MIN_OR_MAX_AMOUNT)
    if (not amt_exists and not min_amt_exists and not max_amt_exists) and filename == 'fare_products.txt':
        line.add_error(NO_AMOUNT_DEFINED)


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
                    messages.add_error(diagnostics.format(NONEXISTENT_AREA_ID, line_num_error_msg, stop_or_stop_time))
                    continue

                if area_id in unused_areas:
                    unused_areas.remove(area_id)


def check_linked_id(line, fieldname, defined_ids):
    if not getattr(line, fieldname):
        return False

    if getattr(line, fieldname) not in defined_ids:
        line.add_error(FOREIGN_ID_INVALID, extra_info=f'{fieldname}: {getattr(line, fieldname)}')

    return True


def check_linked_flr_ftr_entities(line, rider_categories, rider_category_by_fare_container,
                                  linked_entities_by_fare_product):
    if line.fare_product_id and line.fare_product_id not in linked_entities_by_fare_product:
        line.add_error(NONEXISTENT_FARE_PRODUCT_ID)
    if line.rider_category_id and line.rider_category_id not in rider_categories:
        line.add_error(NONEXISTENT_RIDER_CATEGORY_ID)
    if line.fare_container_id and line.fare_container_id not in rider_category_by_fare_container:
        line.add_error(NONEXISTENT_FARE_CONTAINER_ID)

    if line.fare_product_id:
        if line.rider_category_id:
            fp_rider_cats = linked_entities_by_fare_product[line.fare_product_id].get('rider_category_ids')
            if len(fp_rider_cats) and (line.rider_category_id not in fp_rider_cats):
                line.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_PRODUCT)
        if line.fare_container_id:
            fp_fare_containers = linked_entities_by_fare_product[line.fare_product_id].get('fare_container_ids')
            if len(fp_fare_containers) and (line.fare_container_id not in fp_fare_containers):
                line.add_error(CONFLICTING_FARE_CONTAINER_ON_FARE_PRODUCT)
    if line.rider_category_id and line.fare_container_id:
        fc_rider_cat = rider_category_by_fare_container[line.fare_container_id]
        if fc_rider_cat and (fc_rider_cat != line.rider_category_id):
            line.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER)
