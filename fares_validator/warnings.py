# generic warnings
UNEXPECTED_FIELDS = 'A GTFS fares-v2 file has column name(s) not defined in the specification.'
OUTDATED_FIELDS = 'A GTFS fares-v2 file has column name(s) that are outdated and might indicate an invalid dataset.'
UNUSED_AREA_IDS = 'Areas defined in areas.txt are unused in other fares files.'
UNUSED_NETWORK_IDS = 'Networks defined in routes.txt are unused in other fares files.'
UNUSED_TIMEFRAME_IDS = 'Timeframes defined in timeframes.txt are unused in other fares files.'

# areas.txt
NO_AREAS = 'No areas.txt was found, will assume no areas exist.'

# stops.txt
NO_STOPS = 'No stops.txt was found, will assume stops.txt does not reference any areas.'

# stop_areas.txt
NO_STOP_AREAS = 'No stop_areas.txt was found, will assume no areas are associated to stops.'

# routes.txt
NO_ROUTES = 'No routes.txt was found, will assume no networks exist.'

# calendar.txt, calendar_dates.txt
NO_SERVICE_IDS = 'Neither calendar.txt or calendar_dates.txt was found, will assume no service_ids for fares data.'

# timeframes.txt
NO_TIMEFRAMES = 'No timeframes.txt was found, will assume no timeframes exist.'

# rider_categories.txt
MAX_AGE_LESS_THAN_MIN_AGE = 'An entry in rider_categories.txt has max_age less than or equal to min_age.'
NO_RIDER_CATEGORIES = 'No rider_categories.txt was found, will assume no rider_categories exist.'
VERY_LARGE_MAX_AGE = 'An entry in rider_categories.txt has a very large max_age.'
VERY_LARGE_MIN_AGE = 'An entry in rider_categories.txt has a very large min_age.'

# fare_containers.txt
NO_FARE_CONTAINERS = 'No fare_containers.txt was found, will assume no fare_containers exist.'

# fare_products.txt
NO_FARE_PRODUCTS = 'No fare_products.txt was found, will assume no fare_products exist.'
OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT = 'An offset_amount in fare_products.txt is defined without an offset_unit, so duration_unit will be used.'

# fare_leg_rules.txt
NO_FARE_LEG_RULES = 'No fare_leg_rules.txt was found, will assume no fare_leg_rules exist.'

# fare_transfer_rules.txt
NO_FARE_TRANSFER_RULES = 'No fare_transfer_rules.txt was found, will assume no fare_transfer_rules exist.'
UNUSED_LEG_GROUPS = 'Leg groups defined in fare_leg_rules.txt are unused in fare_transfer_rules.txt.'
TRANSFER_COUNT_WITH_EMPTY_LEGS = 'An entry in fare_transfer_rules.txt has transfer_count with empty from and to leg group ids. This may create undefined behaviour.'
