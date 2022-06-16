import csv
from pathlib import Path
from collections import deque, Counter

from . import diagnostics
from .decimals_by_currency import decimals_by_currency
from .errors import *
from .warnings import *


class Schema:
    FAKE_FIELDS = {'line_num_error_msg'}

    def __init__(self,
                 basename,
                 required_fields,
                 defined_fields,
                 *,
                 experimental_fields=set(),
                 experimental=False,
                 message_if_missing=None,
                 suppress_undefined_field_warning=False):
        self.basename = basename
        self.required_fields = required_fields
        self.defined_fields = defined_fields
        self.experimental_fields = experimental_fields
        self.experimental = experimental
        self.valid_fields = self.defined_fields | self.required_fields | self.experimental_fields | Schema.FAKE_FIELDS
        self.message_if_missing = message_if_missing
        self.suppress_undefined_field_warning = suppress_undefined_field_warning

    def has_field(self, field_name, experimental=False):
        if not experimental:
            return field_name in self.defined_fields | self.required_fields | Schema.FAKE_FIELDS
        return field_name in self.valid_fields


class Entity:

    def __init__(self, schema, messages, original_dict, experimental):
        self._schema = schema
        self._messages = messages
        self._data = original_dict
        self._experimental = experimental

    def __getattr__(self, item):
        if self._schema.has_field(item, self._experimental):
            return self._data.get(item)
        else:
            raise TypeError(f'Reference to undefined field {item} in code!')

    def add_error(self, code, experimental=False, extra_info=''):
        self._messages.add_error(
            diagnostics.format(code, self.line_num_error_msg,
                               self._schema.basename, extra_info), experimental)

    def add_warning(self, code, experimental=False, extra_info=''):
        self._messages.add_warning(
            diagnostics.format(code, self.line_num_error_msg,
                               self._schema.basename, extra_info), experimental)


def read_csv_file(gtfs_root_dir, schema, messages, read_experimental=False):
    path = gtfs_root_dir / schema.basename

    if not path.exists():
        if not schema.experimental or read_experimental:
            if schema.message_if_missing and not schema.experimental:
                messages.add_warning(
                    diagnostics.format(schema.message_if_missing))
            elif schema.message_if_missing:
                messages.add_warning(
                    diagnostics.format(schema.message_if_missing), True)
        return []

    with open(path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)

        for required_field in schema.required_fields:
            if required_field not in reader.fieldnames:
                if schema.experimental and read_experimental:
                    messages.add_error(
                        diagnostics.format(REQUIRED_FIELD_MISSING, '',
                                           schema.basename,
                                           f'field:  {required_field}'), True)
                else:
                    messages.add_error(
                        diagnostics.format(REQUIRED_FIELD_MISSING, '',
                                           schema.basename,
                                           f'field:  {required_field}'))
                return []

        if schema.defined_fields and not schema.suppress_undefined_field_warning:
            unexpected_fields = []
            for field in reader.fieldnames:
                if field not in schema.defined_fields:
                    if field not in schema.experimental_fields:
                        unexpected_fields.append(field)
                    elif field in schema.experimental_fields and not read_experimental:
                        unexpected_fields.append(field)
            if 'rider_category_id' in unexpected_fields:
                if schema.basename == 'fare_leg_rules.txt':
                    messages.add_warning(RIDER_CATEGORY_IN_LEG_RULES)
                if schema.basename == 'fare_transfer_rules.txt':
                    messages.add_warning(RIDER_CATEGORY_IN_TRANSFER_RULES)
                unexpected_fields.remove('rider_category_id')
            if 'fare_container_id' in unexpected_fields:
                if schema.basename == 'fare_leg_rules.txt':
                    messages.add_warning(FARE_CONTAINER_IN_LEG_RULES)
                if schema.basename == 'fare_transfer_rules.txt':
                    messages.add_warning(FARE_CONTAINER_IN_TRANSFER_RULES)
                unexpected_fields.remove('fare_container_id')
            if len(unexpected_fields):
                messages.add_warning(
                    diagnostics.format(UNEXPECTED_FIELDS, '', schema.basename,
                                       f'\nColumn(s): {unexpected_fields}'))

        for line in reader:
            line['line_num_error_msg'] = f'\nLine: {reader.line_num}'
            entity = Entity(schema, messages, line, read_experimental)
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
        line.add_error(AMOUNT_WITH_MIN_OR_MAX_AMOUNT, True)
    if (min_amt_exists and not max_amt_exists) or (max_amt_exists and
                                                   not min_amt_exists):
        line.add_error(MISSING_MIN_OR_MAX_AMOUNT, True)
    if (not amt_exists and not min_amt_exists and
            not max_amt_exists) and filename == 'fare_products.txt':
        line.add_error(NO_AMOUNT_DEFINED)


def check_linked_id(line, fieldname, defined_ids, experimental=False):
    if not getattr(line, fieldname):
        return False

    if getattr(line, fieldname) not in defined_ids:
        line.add_error(FOREIGN_ID_INVALID,
                       experimental,
                       extra_info=f'{fieldname}: {getattr(line, fieldname)}')

    return True
