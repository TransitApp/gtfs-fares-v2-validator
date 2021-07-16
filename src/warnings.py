# generic warnings
UNUSED_AREA_IDS = 'Areas defined in areas.txt are unused in other fares files.'
UNUSED_NETWORK_IDS = 'Networks defined in routes.txt are unused in other fares files.'
UNUSED_TIMEFRAME_IDS = 'Timeframes defined in timeframes.txt are unused in other fares files.'

# routes.txt
NO_ROUTES = 'No routes.txt was found, will assume no networks exist.'

# stops.txt
NO_STOPS = 'No stops.txt was found. Will assume stops.txt does not reference any areas.'
UNUSED_AREAS_IN_STOPS = 'Areas defined in areas.txt are unused in stops.txt or stop_times.txt.'

# calendar.txt, calendar_dates.txt
NO_SERVICE_IDS = 'Neither calendar.txt or calendar_dates.txt was found, will assume no service_ids for fares data.'

# rider_categories.txt
MAX_AGE_LESS_THAN_MIN_AGE = 'An entry in rider_categories.txt has max_age less than or equal to min_age.'
VERY_LARGE_MAX_AGE = 'An entry in rider_categories.txt has a very large max_age.'
VERY_LARGE_MIN_AGE = 'An entry in rider_categories.txt has a very large min_age.'

# fare_products.txt
OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT = 'An offset_amount in fare_products.txt is defined without an offset_unit, so duration_unit will be used.'

# fare_transfer_rules.txt
UNUSED_LEG_GROUPS = 'Leg groups defined in fare_leg_rules.txt are unused in fare_transfer_rules.txt.'

def add_warning(warning, line_num_error_msg, warnings, path='', extra_info=''):
    warning_msg = ''
    if path:
        warning_msg += path + ': '
    warning_msg += warning
    if extra_info:
        warning_msg += '\n' + extra_info
    warning_msg += line_num_error_msg

    warnings.append(warning_msg)