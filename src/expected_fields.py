EXPECTED_AREAS_FIELDS = [
    'area_id',
    'area_name',
    'greater_area_id'
]

EXPECTED_TIMEFRAMES_FIELDS = [
    'timeframe_id',
    'start_time',
    'end_time'
]

EXPECTED_RIDER_CATEGORIES_FIELDS = [
    'rider_category_id',
    'min_age',
    'max_age',
    'rider_category_name',
    'eligibility_url'
]

EXPECTED_FARE_CONTAINERS_FIELDS = [
    'fare_container_id',
    'fare_container_name',
    'minimum_initial_purchase',
    'amount',
    'currency',
    'rider_category_id'
]

EXPECTED_FARE_PRODUCTS_FIELDS = [
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
]

EXPECTED_FARE_LEG_RULES_FIELDS = [
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
]

EXPECTED_FARE_TRANSFER_RULES_FIELDS = [
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
]