from fares_validator.loader import run_validator
from fares_validator import errors
from pathlib import Path

test_data_dir = Path(__file__).parent / 'test_data' 

def test_errors_simple_files():
    results = run_validator(test_data_dir / 'bad_gtfs_simple', True)
    
    # Areas errors
    assert errors.EMPTY_AREA_ID in results.errors[0]
    assert errors.DUPLICATE_AREAS_TXT_ENTRY in results.errors[1]
    assert errors.GREATER_AREA_ID_LOOP in results.errors[2]

    # Calendar errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR in results.errors[3]
    assert errors.DUPLICATE_SERVICE_ID in results.errors[4]
    
    # Calendar dates errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR_DATES in results.errors[5]

    # Timeframes errors
    assert errors.INVALID_TIME_FORMAT in results.errors[6]
    assert errors.INVALID_TIME_FORMAT in results.errors[7]
    assert errors.EMPTY_START_TIME in results.errors[8]
    assert errors.EMPTY_END_TIME in results.errors[9]
    assert errors.EMPTY_TIMEFRAME_ID in results.errors[10]

    # Rider categories errors
    assert errors.EMPTY_RIDER_CATEGORY_ID in results.errors[11]
    assert errors.NEGATIVE_MIN_AGE in results.errors[12]
    assert errors.NEGATIVE_MAX_AGE in results.errors[13]
    assert errors.NON_INT_MIN_AGE in results.errors[14]
    assert errors.NON_INT_MAX_AGE in results.errors[15]

    # Fare containers errors
    assert errors.EMPTY_FARE_CONTAINER_ID in results.errors[16]
    assert errors.EMPTY_FARE_CONTAINER_NAME in results.errors[17]
    assert errors.NONEXISTENT_RIDER_CATEGORY_ID in results.errors[18]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[19]
    assert errors.INVALID_AMOUNT_FORMAT in results.errors[20]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[21]
    assert errors.INVALID_AMOUNT_FORMAT in results.errors[22]
    assert errors.CURRENCY_WITHOUT_AMOUNT in results.errors[23]
    assert errors.DUPLICATE_FARE_CONTAINER_ID in results.errors[24]

    assert len(results.errors) == 25

def test_errors_fare_products():
    results = run_validator(test_data_dir / 'bad_fare_products', False)

    assert errors.EMPTY_FARE_PRODUCT_ID in results.errors[0]
    assert errors.EMPTY_FARE_PRODUCT_NAME in results.errors[1]
    assert errors.MISSING_MIN_OR_MAX_AMOUNT in results.errors[2]
    assert errors.AMOUNT_WITH_MIN_OR_MAX_AMOUNT in results.errors[3]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[4]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[5]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[6] # this also is for line 7 of fare products
    assert errors.NO_AMOUNT_DEFINED in results.errors[7]
    assert errors.FOREIGN_ID_INVALID in results.errors[8]
    assert errors.INVALID_TIMEFRAME_TYPE in results.errors[9]
    assert errors.INVALID_TIMEFRAME_TYPE in results.errors[10]
    assert errors.FOREIGN_ID_INVALID in results.errors[11]
    assert errors.TIMEFRAME_TYPE_WITHOUT_TIMEFRAME in results.errors[12]

    assert len(results.errors) == 13

def test_errors_fare_leg_rules():
    results = run_validator(test_data_dir / 'bad_fare_leg_rules', False)

    # check areas
    assert errors.AREA_WITHOUT_IS_SYMMETRICAL in results.errors[0]
    assert errors.CONTAINS_AREA_WITHOUT_FROM_TO_AREA in results.errors[1]
    assert errors.IS_SYMMETRICAL_WITHOUT_FROM_TO_AREA in results.errors[2]
    assert errors.INVALID_IS_SYMMETRICAL_LEG_RULES in results.errors[3]
    assert errors.FOREIGN_ID_INVALID in results.errors[4]

    # check networks
    assert errors.FOREIGN_ID_INVALID in results.errors[5]

    # check timeframes
    assert errors.FOREIGN_ID_INVALID in results.errors[6]
    assert errors.FOREIGN_ID_INVALID in results.errors[7]

    # check service_id
    assert errors.FOREIGN_ID_INVALID in results.errors[8]

    # check distances
    assert errors.INVALID_MIN_DISTANCE in results.errors[9]
    assert errors.INVALID_MAX_DISTANCE in results.errors[10]
    assert errors.DISTANCE_WITHOUT_DISTANCE_TYPE in results.errors[11]
    assert errors.INVALID_DISTANCE_TYPE in results.errors[12]
    assert errors.NEGATIVE_MIN_DISTANCE in results.errors[13]
    assert errors.NEGATIVE_MAX_DISTANCE in results.errors[14]
    assert errors.DISTANCE_TYPE_WITHOUT_DISTANCE in results.errors[15]

    # check amounts/fare_product/fare_leg_name
    assert errors.CURRENCY_WITHOUT_AMOUNT in results.errors[16]
    assert errors.AMOUNT_WITH_FARE_PRODUCT in results.errors[17]
    assert errors.AMOUNT_WITH_MIN_OR_MAX_AMOUNT in results.errors[18]
    assert errors.MISSING_MIN_OR_MAX_AMOUNT in results.errors[19]
    assert errors.FARE_LEG_NAME_WITH_FARE_PRODUCT in results.errors[20]

    # check linked entities
    assert errors.NONEXISTENT_FARE_PRODUCT_ID in results.errors[21]
    assert errors.NONEXISTENT_RIDER_CATEGORY_ID in results.errors[22]
    assert errors.NONEXISTENT_FARE_CONTAINER_ID in results.errors[23]
    assert errors.CONFLICTING_RIDER_CATEGORY_ON_FARE_PRODUCT in results.errors[24]
    assert errors.CONFLICTING_FARE_CONTAINER_ON_FARE_PRODUCT in results.errors[25]
    assert errors.CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER in results.errors[26]

    assert len(results.errors) == 27

def test_errors_fare_transfer_rules():
    results = run_validator(test_data_dir / 'bad_fare_transfer_rules', False)

    # check leg groups
    assert errors.IS_SYMMETRICAL_WITHOUT_FROM_TO_LEG_GROUP in results.errors[0]
    assert errors.LEG_GROUP_WITHOUT_IS_SYMMETRICAL in results.errors[1]
    assert errors.INVALID_IS_SYMMETRICAL_TRANSFER_RULES in results.errors[2]
    assert errors.INVALID_TO_LEG_GROUP in results.errors[3]
    assert errors.INVALID_FROM_LEG_GROUP in results.errors[4]

    # check transfer_id and spans
    assert errors.SPANNING_LIMIT_WITH_BAD_LEGS in results.errors[5]
    assert errors.INVALID_SPANNING_LIMIT in results.errors[6]
    assert errors.INVALID_SPANNING_LIMIT in results.errors[7]
    assert errors.SPANNING_LIMIT_WITH_TRANSFER_ID in results.errors[8]
    assert errors.TRANSFER_ID_WITHOUT_TRANSFER_SEQUENCE in results.errors[9]
    assert errors.TRANSFER_SEQUENCE_WITHOUT_TRANSFER_ID in results.errors[10]
    assert errors.INVALID_TRANSFER_SEQUENCE in results.errors[11]
    assert errors.INVALID_TRANSFER_SEQUENCE in results.errors[12]

    # check durations
    assert errors.INVALID_DURATION_LIMIT_TYPE in results.errors[13]
    assert errors.DURATION_LIMIT_WITHOUT_LIMIT_TYPE in results.errors[14]
    assert errors.INVALID_DURATION_LIMIT in results.errors[15]
    assert errors.DURATION_LIMIT_TYPE_WITHOUT_DURATION in results.errors[16]

    # check amounts
    assert errors.CURRENCY_WITHOUT_AMOUNT in results.errors[17]
    assert errors.AMOUNT_WITHOUT_CURRENCY in results.errors[18]
    assert errors.AMOUNT_WITHOUT_FARE_TRANSFER_TYPE in results.errors[19]
    assert errors.INVALID_FARE_TRANSFER_TYPE in results.errors[20]
    assert errors.UNRECOGNIZED_CURRENCY_CODE in results.errors[21]
    assert errors.FARE_TRANSFER_TYPE_WITHOUT_AMOUNT in results.errors[22]

    # check linked entities
    assert errors.NONEXISTENT_FARE_PRODUCT_ID in results.errors[23]
    assert errors.NONEXISTENT_RIDER_CATEGORY_ID in results.errors[24]
    assert errors.NONEXISTENT_FARE_CONTAINER_ID in results.errors[25]
    assert errors.CONFLICTING_RIDER_CATEGORY_ON_FARE_PRODUCT in results.errors[26]
    assert errors.CONFLICTING_FARE_CONTAINER_ON_FARE_PRODUCT in results.errors[27]
    assert errors.CONFLICTING_RIDER_CATEGORY_ON_FARE_CONTAINER in results.errors[28]

    assert len(results.errors) == 29

def test_required_fields():
    results = run_validator(test_data_dir / 'required_fields_test', False)

    assert errors.REQUIRED_FIELD_MISSING in results.errors[0]
    assert 'areas.txt' in results.errors[0]
    
    assert errors.REQUIRED_FIELD_MISSING in results.errors[1]
    assert 'calendar.txt' in results.errors[1]

    assert errors.REQUIRED_FIELD_MISSING in results.errors[2]
    assert 'calendar_dates.txt' in results.errors[2]

    assert errors.REQUIRED_FIELD_MISSING in results.errors[3]
    assert 'timeframes.txt' in results.errors[3]

    assert errors.REQUIRED_FIELD_MISSING in results.errors[4]
    assert 'rider_categories.txt' in results.errors[4]

    assert errors.REQUIRED_FIELD_MISSING in results.errors[5]
    assert 'fare_containers.txt' in results.errors[5]

    assert errors.REQUIRED_FIELD_MISSING in results.errors[6]
    assert 'fare_products.txt' in results.errors[6]

    assert len(results.errors) == 7
