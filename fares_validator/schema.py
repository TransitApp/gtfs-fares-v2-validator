from . import warnings
from .utils import Schema

AREAS = Schema('areas.txt',
               required_fields={'area_id'},
               defined_fields={
                   'area_id',
                   'area_name',
                   'greater_area_id'
               }, message_if_missing=warnings.NO_AREAS)

ROUTES = Schema('routes.txt', set(), {'network_id'},
                message_if_missing=warnings.NO_ROUTES,
                suppress_undefined_field_warning=True)

CALENDAR = Schema('calendar.txt', {'service_id'}, set())

CALENDAR_DATES = Schema('calendar_dates.txt', {'service_id'}, set())

TIMEFRAMES = Schema('timeframes.txt', {'timeframe_id', 'start_time', 'end_time'}, {
    'timeframe_id',
    'start_time',
    'end_time'
}, message_if_missing=warnings.NO_TIMEFRAMES)

RIDER_CATEGORIES = Schema('rider_categories.txt', {'rider_category_id'}, {
    'rider_category_id',
    'min_age',
    'max_age',
    'rider_category_name',
    'eligibility_url'
}, message_if_missing=warnings.NO_RIDER_CATEGORIES)

FARE_CONTAINERS = Schema('fare_containers.txt', {'fare_container_id', 'fare_container_name'}, {
    'fare_container_id',
    'fare_container_name',
    'minimum_initial_purchase',
    'amount',
    'currency',
    'rider_category_id'
}, message_if_missing=warnings.NO_FARE_CONTAINERS)

FARE_PRODUCTS = Schema('fare_products.txt', {'fare_product_id', 'fare_product_name'}, {
    'fare_product_id',
    'fare_product_name',
    'rider_category_id',
    'fare_container_id',
    'bundle_amount',
    'duration_start',
    'duration_amount',
    'duration_unit',
    'duration_type',
    'offset_amount',
    'offset_unit',
    'service_id',
    'timeframe_id',
    'timeframe_type',
    'cap_required',
    'eligible_cap_id',
    'amount',
    'min_amount',
    'max_amount',
    'currency'
}, message_if_missing=warnings.NO_FARE_PRODUCTS)

FARE_LEG_RULES = Schema('fare_leg_rules.txt', set(), {
    'leg_group_id',
    'fare_leg_name',
    'network_id',
    'from_area_id',
    'contains_area_id',
    'to_area_id',
    'is_symmetrical',
    'from_timeframe_id',
    'to_timeframe_id',
    'min_distance',
    'max_distance',
    'distance_type',
    'service_id',
    'amount',
    'min_amount',
    'max_amount',
    'currency',
    'fare_product_id',
    'fare_container_id',
    'rider_category_id',
    'eligible_cap_id'
})

FARE_TRANSFER_RULES = Schema('fare_transfer_rules.txt', set(), {
    'from_leg_group_id',
    'to_leg_group_id',
    'is_symmetrical',
    'spanning_limit',
    'transfer_id',
    'transfer_sequence',
    'duration_limit',
    'duration_limit_type',
    'fare_transfer_type',
    'amount',
    'min_amount',
    'max_amount',
    'currency',
    'fare_product_id',
    'fare_container_id',
    'rider_category_id',
    'eligible_cap_id'
})
