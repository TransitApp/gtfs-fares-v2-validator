# generic errors (see utils.py)
AMOUNT_WITH_MIN_OR_MAX_AMOUNT = 'An amount is defined alongside at least one of min_ or max_amount.'
AMOUNT_WITHOUT_CURRENCY = 'An amount field is defined without a currency to accompany it.'
CONFLICTING_FARE_CONTAINER_ON_FARE_PRODUCT = 'A fare_container referenced conflicts with the fare_container on the fare_product.'
CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER = 'A rider_category referenced conflicts with the rider_category on the fare_container.'
CONFLICTING_RIDER_CATEGORY_ON_FARE_PRODUCT = 'A rider_category referenced conflicts with the rider_category on the fare_product.'
CURRENCY_WITHOUT_AMOUNT = 'A currency is defined without an amount field to accompany it.'
FOREIGN_ID_INVALID = 'An id defined in a dependent table is referenced, but does not exist in that table.'
INVALID_AMOUNT_FORMAT = 'An amount field is defined, but is not an integer or float.'
MISSING_MIN_OR_MAX_AMOUNT = 'A min_ or max_amount is defined without its complement.'
NONEXISTENT_AREA_ID = 'An area_id referenced is not defined in areas.txt.'
NONEXISTENT_FARE_CONTAINER_ID = 'A fare_container referenced is not defined in fare_containers.txt.'
NONEXISTENT_FARE_PRODUCT_ID = 'A fare_product referenced is not defined in fare_products.txt.'
NONEXISTENT_RIDER_CATEGORY_ID = 'A rider_category referenced is not defined in rider_categories.txt.'
REQUIRED_FIELD_MISSING = 'A required field is missing from the header.'
TOO_MANY_AMOUNT_DECIMALS = 'An amount field has many decimals for the currency defined.'
UNRECOGNIZED_CURRENCY_CODE = 'A currency code is unrecognized.'

# areas.txt
DUPLICATE_AREA_ID = 'An area_id is defined twice in areas.txt.'
EMPTY_AREA_ID = 'An entry in areas.txt has empty area id.'
GREATER_AREA_ID_LOOP = 'An area_id has itself as a greater_area_id.'
UNDEFINED_GREATER_AREA_ID = 'A greater_area_id is not defined as an area_id in areas.txt.'

# calendar.txt, calendar_dates.txt
DUPLICATE_SERVICE_ID = 'A service_id is defined twice in calendar.txt.'
EMPTY_SERVICE_ID_CALENDAR = 'An entry in calendar.txt has empty service_id.'
EMPTY_SERVICE_ID_CALENDAR_DATES = 'An entry in calendar_dates.txt has empty service_id.'

# timeframes.txt
EMPTY_END_TIME = 'An entry in timeframes.txt has empty end_time.'
EMPTY_START_TIME = 'An entry in timeframes.txt has empty start_time.'
EMPTY_TIMEFRAME_ID = 'An entry in timeframes.txt has empty timeframe_id.'
INVALID_TIME_FORMAT = 'An entry in timeframes.txt has an invalid time format.'

# rider_categories.txt
EMPTY_RIDER_CATEGORY_ID = 'An entry in rider_categories.txt has empty rider_category_id.'
NON_INT_MAX_AGE = 'An entry in rider_categories.txt has non-integer max_age.'
NON_INT_MIN_AGE = 'An entry in rider_categories.txt has non-integer min_age.'
NEGATIVE_MAX_AGE = 'An entry in rider_categories.txt has negative max_age.'
NEGATIVE_MIN_AGE = 'An entry in rider_categories.txt has negative min_age.'

# fare_containers.txt
DUPLICATE_FARE_CONTAINER_ID = 'An fare_container_id is defined twice in fare_containers.txt.'
EMPTY_FARE_CONTAINER_ID = 'An entry in fare_containers.txt has empty fare_container_id.'
EMPTY_FARE_CONTAINER_NAME = 'An entry in fare_containers.txt has empty fare_container_name.'

# fare_products.txt
DURATION_START_WITH_DURATION_TYPE = 'A duration_start in fare_products.txt is defined with duration_type=1.'
DURATION_TYPE_WITHOUT_AMOUNT = 'A duration_type in fare_products.txt is defined without duration_amount.'
DURATION_UNIT_WITHOUT_AMOUNT = 'A duration_unit in fare_products.txt is defined without duration_amount.'
DURATION_WITHOUT_TYPE = 'A duration_amount in fare_products.txt is defined without duration_type.'
DURATION_WITHOUT_UNIT = 'A duration_amount in fare_products.txt is defined without duration_unit.'
EMPTY_FARE_PRODUCT_ID = 'An entry in fare_products.txt has empty fare_product_id.'
EMPTY_FARE_PRODUCT_NAME = 'An entry in fare_products.txt has empty fare_product_name.'
INVALID_BUNDLE_AMOUNT = 'A bundle_amount in fare_products.txt has an invalid value.'
INVALID_DURATION_START = 'A duration_start in fare_products.txt is not one of the accepted values.'
INVALID_DURATION_TYPE = 'A duration_type in fare_products.txt is not one of the accepted values.'
INVALID_DURATION_UNIT = 'A duration_unit in fare_products.txt is not one of the accepted values.'
INVALID_OFFSET_UNIT = 'A offset_unit in fare_products.txt is not one of the accepted values.'
INVALID_TIMEFRAME_TYPE = 'A timeframe_type in fare_products.txt has an invalid value, or is required and does not exist.'
NEGATIVE_OR_ZERO_DURATION = 'A duration_amount in fare_products.txt is 0 or negative.'
NO_AMOUNT_DEFINED = 'An entry in fare_products.txt does not have any amount, min_amount, or max_amount.'
NON_INT_DURATION_AMOUNT = 'A duration_amount in fare_products.txt is not an integer.'
NON_INT_OFFSET_AMOUNT = 'An offset_amount in fare_products.txt is not an integer.'
OFFSET_AMOUNT_WITH_DURATION_TYPE = 'An offset_amount in fare_products.txt is defined for duration_type=2.'
OFFSET_UNIT_WITHOUT_AMOUNT = 'An offset_unit in fare_products.txt is defined without an offset_amount.'
TIMEFRAME_TYPE_WITHOUT_TIMEFRAME = 'A timeframe_type in fare_products.txt is defined without a timeframe_id.'

# fare_leg_rules.txt
AMOUNT_WITH_FARE_PRODUCT = 'An entry in fare_leg_rules.txt has both a fare_product and an amount field defined.'
AREA_WITHOUT_IS_SYMMETRICAL = 'A from_ and/or to_area in fare_leg_rules.txt is defined without is_symmetrical.'
CONTAINS_AREA_WITHOUT_FROM_TO_AREA = 'A contains_area in fare_leg_rules.txt is defined without a from and to area.'
DISTANCE_TYPE_WITHOUT_DISTANCE = 'A distance_type in fare_leg_rules.txt is defined without a min_ or max_distance.'
DISTANCE_WITHOUT_DISTANCE_TYPE = 'A min_ or max_distance in fare_leg_rules.txt is defined without a distance_type.'
FARE_LEG_NAME_WITH_FARE_PRODUCT = 'An entry in fare_leg_rules.txt has both a fare_product and a fare_leg_name field defined.'
INVALID_DISTANCE_TYPE = 'A distance_type in fare_leg_rules.txt has an invalid value.'
INVALID_IS_SYMMETRICAL_LEG_RULES = 'An is_symmetrical in fare_leg_rules.txt is not one of the accepted values.'
INVALID_MAX_DISTANCE = 'A max_distance in fare_leg_rules.txt is not a float.'
INVALID_MIN_DISTANCE = 'A min_distance in fare_leg_rules.txt is not a float.'
IS_SYMMETRICAL_WITHOUT_FROM_TO_AREA = 'An is_symmetrical in fare_leg_rules.txt is defined without a from_ and/or to_area.'
NEGATIVE_MAX_DISTANCE = 'A max_distance in fare_leg_rules.txt is negative.'
NEGATIVE_MIN_DISTANCE = 'A min_distance in fare_leg_rules.txt is negative.'

# fare_transfer_rules.txt
AMOUNT_WITHOUT_FARE_TRANSFER_TYPE = 'An entry in fare_transfer_rules.txt has an amount field defined without fare_transfer_type.'
DURATION_LIMIT_WITHOUT_LIMIT_TYPE = 'An entry in fare_transfer_rules.txt has duration_limit without duration_limit_type.'
DURATION_LIMIT_TYPE_WITHOUT_DURATION = 'An entry in fare_transfer_rules.txt has duration_limit_type without duration_limit.'
FARE_TRANSFER_TYPE_WITHOUT_AMOUNT = 'An entry in fare_transfer_rules.txt has fare_transfer_type defined without an amount field.'
INVALID_DURATION_LIMIT = 'An entry in fare_transfer_rules.txt has duration_limit with invalid value.'
INVALID_DURATION_LIMIT_TYPE = 'An entry in fare_transfer_rules.txt has duration_limit_type with invalid value.'
INVALID_FARE_TRANSFER_TYPE = 'An entry in fare_transfer_rules.txt has fare_transfer_type with invalid value.'
INVALID_FROM_LEG_GROUP = 'A from_leg_group_id in fare_transfer_rules.txt is not defined in fare_leg_rules.txt.'
INVALID_IS_SYMMETRICAL_TRANSFER_RULES = 'An is_symmetrical in fare_transfer_rules.txt is not one of the accepted values.'
INVALID_SPANNING_LIMIT = 'An entry in fare_transfer_rules.txt has spanning_limit with incorrect type or invalid integer value.'
INVALID_TO_LEG_GROUP = 'A to_leg_group_id in fare_transfer_rules.txt is not defined in fare_leg_rules.txt.'
INVALID_TRANSFER_SEQUENCE = 'A transfer_sequence in fare_transfer_rules.txt has incorrect type or invalid integer value.'
IS_SYMMETRICAL_WITHOUT_FROM_TO_LEG_GROUP = 'An is_symmetrical in fare_transfer_rules.txt is defined without a from_ and/or to_leg_group_id.'
LEG_GROUP_WITHOUT_IS_SYMMETRICAL = 'A from_ and/or to_leg_group_id in fare_transfer_rules.txt is defined without is_symmetrical.'
SPANNING_LIMIT_WITH_BAD_LEGS = 'An entry in fare_transfer_rules.txt has spanning_limit with different from and to leg group ids.'
SPANNING_LIMIT_WITH_TRANSFER_ID = 'An entry in fare_transfer_rules.txt has spanning_limit with transfer_id defined.'
TRANSFER_ID_WITHOUT_TRANSFER_SEQUENCE = 'A transfer_id in fare_transfer_rules.txt is defined without a transfer_sequence.'
TRANSFER_SEQUENCE_WITHOUT_TRANSFER_ID = 'A transfer_sequence in fare_transfer_rules.txt is defined without a transfer_id.'
