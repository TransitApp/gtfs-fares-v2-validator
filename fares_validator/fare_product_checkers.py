from .errors import *
from .warnings import *


class LinkedEntities:
    def __init__(self):
        self.rider_category_ids = set()
        self.fare_container_ids = set()


def check_linked_fp_entities(line, rider_categories, rider_category_by_fare_container, linked_entities_by_fare_product):
    linked_entities = linked_entities_by_fare_product.setdefault(line.fare_product_id, LinkedEntities())

    if line.rider_category_id:
        linked_entities.rider_category_ids.add(line.rider_category_id)
        if line.rider_category_id not in rider_categories:
            line.add_error(NONEXISTENT_RIDER_CATEGORY_ID)

    if line.fare_container_id:
        linked_entities.fare_container_ids.add(line.fare_container_id)
        if line.fare_container_id not in rider_category_by_fare_container:
            line.add_error(NONEXISTENT_FARE_CONTAINER_ID)

        fare_container_rider_cat = rider_category_by_fare_container.get(line.fare_container_id)
        if line.rider_category_id and fare_container_rider_cat and (line.rider_category_id != fare_container_rider_cat):
            line.add_error(CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER)

    linked_entities_by_fare_product[line.fare_product_id] = linked_entities


def check_bundle(line):
    if line.bundle_amount:
        try:
            bundle_amt = int(line.bundle_amount)
            if bundle_amt < 0:
                line.add_error(INVALID_BUNDLE_AMOUNT)
        except ValueError:
            line.add_error(INVALID_BUNDLE_AMOUNT)


def check_durations_and_offsets(line):
    if line.duration_start and line.duration_start not in {'0', '1'}:
        line.add_error(INVALID_DURATION_START)

    if line.duration_unit and line.duration_unit not in {'0', '1', '2', '3', '4', '5', '6'}:
        line.add_error(INVALID_DURATION_UNIT)

    if line.duration_type and line.duration_type in {'1', '2'}:
        line.add_error(INVALID_DURATION_TYPE)

    if line.duration_type == '1' and line.duration_start:
        line.add_error(DURATION_START_WITH_DURATION_TYPE)

    if line.duration_amount:
        try:
            amt = int(line.duration_amount)
            if amt < 1:
                line.add_error(NEGATIVE_OR_ZERO_DURATION)
        except ValueError:
            line.add_error(NON_INT_DURATION_AMOUNT)

        if not line.duration_unit:
            line.add_error(DURATION_WITHOUT_UNIT)

        if not line.duration_type:
            line.add_error(DURATION_WITHOUT_TYPE)
    else:
        if line.duration_type:
            line.add_error(DURATION_TYPE_WITHOUT_AMOUNT)
        if line.duration_unit:
            line.add_error(DURATION_UNIT_WITHOUT_AMOUNT)

    if line.offset_unit and line.offset_unit not in {'0', '1', '2', '3', '4', '5', '6'}:
        line.add_error(INVALID_OFFSET_UNIT, line.line_num_error_msg)

    if line.offset_amount:
        try:
            amt = int(line.offset_amount)
        except ValueError:
            line.add_error(NON_INT_OFFSET_AMOUNT)

        if line.duration_type == '2':
            line.add_error(OFFSET_AMOUNT_WITH_DURATION_TYPE)

        if not line.offset_unit:
            line.add_warning(OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT)
    else:
        if line.offset_unit:
            line.add_error(OFFSET_UNIT_WITHOUT_AMOUNT)
