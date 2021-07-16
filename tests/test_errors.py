from run_validator import run_validator
from src import errors
from os import path

def test_errors_simple_files():
    results = run_validator(path.join('tests', 'test_data', 'bad_gtfs_simple'), True)
    errors_list = results['errors']
    
    # Areas errors
    assert errors.DUPLICATE_AREA_ID in errors_list[0]
    assert errors.EMPTY_AREA_ID in errors_list[1]
    assert errors.GREATER_AREA_ID_LOOP in errors_list[2]

    # Stops errors
    assert errors.NONEXISTENT_AREA_ID in errors_list[5]

    # Stop times errors
    assert errors.NONEXISTENT_AREA_ID in errors_list[6]

    # Calendar errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR in errors_list[7]
    assert errors.DUPLICATE_SERVICE_ID in errors_list[8]
    
    # Calendar dates errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR_DATES in errors_list[9]

    # Timeframes errors
    assert errors.INVALID_TIME_FORMAT in errors_list[10]
    assert errors.INVALID_TIME_FORMAT in errors_list[11]
    assert errors.EMPTY_START_TIME in errors_list[12]
    assert errors.EMPTY_END_TIME in errors_list[13]
    assert errors.EMPTY_TIMEFRAME_ID in errors_list[14]

    # Rider categories errors
    assert errors.EMPTY_RIDER_CATEGORY_ID in errors_list[15]
    assert errors.NEGATIVE_MIN_AGE in errors_list[16]
    assert errors.NEGATIVE_MAX_AGE in errors_list[17]
    assert errors.NON_INT_MIN_AGE in errors_list[18]
    assert errors.NON_INT_MAX_AGE in errors_list[19]

    # Fare containers errors
    assert errors.EMPTY_FARE_CONTAINER_ID in errors_list[20]
    assert errors.EMPTY_FARE_CONTAINER_NAME in errors_list[21]
    assert errors.NONEXISTENT_RIDER_CATEGORY_ID in errors_list[22]
    assert errors.AMOUNT_WITHOUT_CURRENCY in errors_list[23]
    assert errors.INVALID_AMOUNT_FORMAT in errors_list[24]
    assert errors.AMOUNT_WITHOUT_CURRENCY in errors_list[25]
    assert errors.INVALID_AMOUNT_FORMAT in errors_list[26]
    assert errors.CURRENCY_WITHOUT_AMOUNT in errors_list[27]
    assert errors.DUPLICATE_FARE_CONTAINER_ID in errors_list[28]

    assert len(errors_list) == 29

def test_errors_fare_products():
    results = run_validator(path.join('tests', 'test_data', 'bad_fare_products'), False)
    errors_list = results['errors']

    assert errors.EMPTY_FARE_PRODUCT_ID in errors_list[0]
    assert errors.EMPTY_FARE_PRODUCT_NAME in errors_list[1]
    assert errors.MISSING_MIN_OR_MAX_AMOUNT in errors_list[2]
    assert errors.AMOUNT_WITH_MIN_OR_MAX_AMOUNT in errors_list[3]
    assert errors.AMOUNT_WITHOUT_CURRENCY in errors_list[4]
    assert errors.AMOUNT_WITHOUT_CURRENCY in errors_list[5]
    assert errors.AMOUNT_WITHOUT_CURRENCY in errors_list[6] # this also is for line 7 of fare products
    assert errors.NO_AMOUNT_DEFINED in errors_list[7]
    assert errors.FOREIGN_ID_INVALID in errors_list[8]
    assert errors.INVALID_TIMEFRAME_TYPE in errors_list[9]
    assert errors.INVALID_TIMEFRAME_TYPE in errors_list[10]
    assert errors.FOREIGN_ID_INVALID in errors_list[11]
    assert errors.TIMEFRAME_TYPE_WITHOUT_TIMEFRAME in errors_list[12]

    assert len(errors_list) == 13

def test_required_fields():
    pass