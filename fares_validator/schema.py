from . import warnings
from .utils import Schema

AREAS = Schema('areas.txt',
               required_fields={'area_id'},
               defined_fields={'area_id', 'area_name'},
               message_if_missing=warnings.NO_AREAS)

STOPS = Schema('stops.txt',
               set(), {'stop_id'},
               message_if_missing=warnings.NO_STOPS,
               suppress_undefined_field_warning=True)

STOP_AREAS = Schema('stop_areas.txt',
                    required_fields={'area_id', 'stop_id'},
                    defined_fields={'area_id', 'stop_id'},
                    message_if_missing=warnings.NO_STOP_AREAS)

ROUTES = Schema('routes.txt',
                set(), {'network_id'},
                message_if_missing=warnings.NO_ROUTES,
                suppress_undefined_field_warning=True)

CALENDAR = Schema('calendar.txt', {'service_id'}, set())

CALENDAR_DATES = Schema('calendar_dates.txt', {'service_id'}, set())

TIMEFRAMES = Schema('timeframes.txt',
                    required_fields={'timeframe_id', 'start_time', 'end_time'},
                    defined_fields={'timeframe_id', 'start_time', 'end_time'},
                    experimental=True,
                    message_if_missing=warnings.NO_TIMEFRAMES)

RIDER_CATEGORIES = Schema('rider_categories.txt',
                          required_fields={'rider_category_id'},
                          defined_fields={
                              'rider_category_id', 'min_age', 'max_age',
                              'rider_category_name', 'eligibility_url'
                          },
                          experimental=True,
                          message_if_missing=warnings.NO_RIDER_CATEGORIES)

FARE_CONTAINERS = Schema(
    'fare_containers.txt',
    required_fields={'fare_container_id', 'fare_container_name'},
    defined_fields={
        'fare_container_id', 'fare_container_name', 'minimum_initial_purchase',
        'amount', 'currency', 'rider_category_id'
    },
    experimental=True,
    message_if_missing=warnings.NO_FARE_CONTAINERS)

FARE_PRODUCTS = Schema('fare_products.txt',
                       required_fields={'fare_product_id', 'fare_product_name'},
                       defined_fields={
                           'fare_product_id', 'fare_product_name', 'amount',
                           'currency'
                       },
                       experimental_fields={
                           'min_amount', 'max_amount', 'bundle_amount',
                           'duration_start', 'duration_amount', 'duration_unit',
                           'duration_type', 'offset_amount', 'offset_unit',
                           'fare_container_id', 'rider_category_id'
                       },
                       message_if_missing=warnings.NO_FARE_PRODUCTS)

FARE_LEG_RULES = Schema('fare_leg_rules.txt',
                        required_fields={'fare_product_id'},
                        defined_fields={
                            'leg_group_id', 'network_id', 'from_area_id',
                            'to_area_id', 'fare_product_id'
                        },
                        experimental_fields={
                            'from_timeframe_id', 'to_timeframe_id',
                            'min_distance', 'max_distance', 'distance_type',
                            'service_id', 'fare_leg_name', 'transfer_only'
                        },
                        outdated_fields={
                            'amount', 'currency', 'min_amount', 'max_amount',
                            'rider_category_id', 'fare_container_id'
                        })

FARE_TRANSFER_RULES = Schema('fare_transfer_rules.txt',
                             required_fields={'fare_transfer_type'},
                             defined_fields={
                                 'from_leg_group_id', 'to_leg_group_id',
                                 'transfer_count', 'duration_limit',
                                 'duration_limit_type', 'fare_transfer_type',
                                 'fare_product_id'
                             },
                             experimental_fields={'filter_fare_product_id'},
                             outdated_fields={
                                 'amount', 'currency', 'min_amount',
                                 'max_amount', 'rider_category_id',
                                 'fare_container_id'
                             })
