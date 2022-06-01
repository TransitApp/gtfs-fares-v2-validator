from fares_validator.loader import run_validator
from fares_validator import errors
from pathlib import Path

test_data_dir = Path(__file__).parent / 'test_data'


def test_errors_simple_files():
    results = run_validator(test_data_dir / 'bad_gtfs_simple', True)
    error_iter = results.errors.__iter__()

    # Areas errors
    assert errors.EMPTY_AREA_ID_AREAS in error_iter.__next__()
    assert errors.DUPLICATE_AREAS_TXT_ENTRY in error_iter.__next__()

    # Stop_areas errors
    assert errors.EMPTY_AREA_ID_STOP_AREAS in error_iter.__next__()
    assert errors.EMPTY_STOP_ID_STOP_AREAS in error_iter.__next__()
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()
    assert errors.DUPLICATE_STOP_AREAS_TXT_ENTRY in error_iter.__next__()

    # Calendar errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR in error_iter.__next__()
    assert errors.DUPLICATE_SERVICE_ID in error_iter.__next__()

    # Calendar dates errors
    assert errors.EMPTY_SERVICE_ID_CALENDAR_DATES in error_iter.__next__()

    # Timeframes errors
    assert errors.INVALID_TIME_FORMAT in error_iter.__next__()
    assert errors.INVALID_TIME_FORMAT in error_iter.__next__()
    assert errors.EMPTY_START_TIME in error_iter.__next__()
    assert errors.EMPTY_END_TIME in error_iter.__next__()
    assert errors.EMPTY_TIMEFRAME_ID in error_iter.__next__()

    # Rider categories errors
    assert errors.EMPTY_RIDER_CATEGORY_ID in error_iter.__next__()
    assert errors.NEGATIVE_MIN_AGE in error_iter.__next__()
    assert errors.NEGATIVE_MAX_AGE in error_iter.__next__()
    assert errors.NON_INT_MIN_AGE in error_iter.__next__()
    assert errors.NON_INT_MAX_AGE in error_iter.__next__()

    # Fare containers errors
    assert errors.EMPTY_FARE_CONTAINER_ID in error_iter.__next__()
    assert errors.EMPTY_FARE_CONTAINER_NAME in error_iter.__next__()
    assert errors.NONEXISTENT_RIDER_CATEGORY_ID in error_iter.__next__()
    assert errors.AMOUNT_WITHOUT_CURRENCY in error_iter.__next__()
    assert errors.INVALID_AMOUNT_FORMAT in error_iter.__next__()
    assert errors.AMOUNT_WITHOUT_CURRENCY in error_iter.__next__()
    assert errors.INVALID_AMOUNT_FORMAT in error_iter.__next__()
    assert errors.CURRENCY_WITHOUT_AMOUNT in error_iter.__next__()
    assert errors.DUPLICATE_FARE_CONTAINER_ID in error_iter.__next__()

    try:
        should_not_exist = error_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True


def test_errors_fare_products():
    results = run_validator(test_data_dir / 'bad_fare_products', False)
    error_iter = results.errors.__iter__()

    assert errors.EMPTY_FARE_PRODUCT_ID in error_iter.__next__()
    assert errors.EMPTY_FARE_PRODUCT_NAME in error_iter.__next__()
    assert errors.MISSING_MIN_OR_MAX_AMOUNT in error_iter.__next__()
    assert errors.AMOUNT_WITH_MIN_OR_MAX_AMOUNT in error_iter.__next__()
    assert errors.AMOUNT_WITHOUT_CURRENCY in error_iter.__next__()
    assert errors.AMOUNT_WITHOUT_CURRENCY in error_iter.__next__()
    assert errors.AMOUNT_WITHOUT_CURRENCY in error_iter.__next__(
    )  # this also is for line 7 of fare products
    assert errors.NO_AMOUNT_DEFINED in error_iter.__next__()
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()
    assert errors.INVALID_TIMEFRAME_TYPE in error_iter.__next__()
    assert errors.INVALID_TIMEFRAME_TYPE in error_iter.__next__()
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()
    assert errors.TIMEFRAME_TYPE_WITHOUT_TIMEFRAME in error_iter.__next__()

    try:
        should_not_exist = error_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True


def test_errors_fare_leg_rules():
    results = run_validator(test_data_dir / 'bad_fare_leg_rules', False)
    error_iter = results.errors.__iter__()

    # check areas
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()

    # check networks
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()

    # check timeframes
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()

    # check service_id
    assert errors.FOREIGN_ID_INVALID in error_iter.__next__()

    # check distances
    assert errors.INVALID_MIN_DISTANCE in error_iter.__next__()
    assert errors.INVALID_MAX_DISTANCE in error_iter.__next__()
    assert errors.DISTANCE_WITHOUT_DISTANCE_TYPE in error_iter.__next__()
    assert errors.INVALID_DISTANCE_TYPE in error_iter.__next__()
    assert errors.NEGATIVE_MIN_DISTANCE in error_iter.__next__()
    assert errors.NEGATIVE_MAX_DISTANCE in error_iter.__next__()
    assert errors.DISTANCE_TYPE_WITHOUT_DISTANCE in error_iter.__next__()

    # check amounts/fare_product/fare_leg_name
    assert errors.FARE_LEG_NAME_WITH_FARE_PRODUCT in error_iter.__next__()

    # check linked entities
    assert errors.NONEXISTENT_FARE_PRODUCT_ID in error_iter.__next__()

    try:
        should_not_exist = error_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True


def test_errors_fare_transfer_rules():
    results = run_validator(test_data_dir / 'bad_fare_transfer_rules', False)
    error_iter = results.errors.__iter__()

    # check leg groups
    assert errors.INVALID_TO_LEG_GROUP in error_iter.__next__()
    assert errors.INVALID_FROM_LEG_GROUP in error_iter.__next__()

    # check transfer_id and spans
    assert errors.TRANSFER_COUNT_WITH_BAD_LEGS in error_iter.__next__()
    assert errors.INVALID_TRANSFER_COUNT in error_iter.__next__()
    assert errors.INVALID_TRANSFER_COUNT in error_iter.__next__()

    # check durations
    assert errors.INVALID_DURATION_LIMIT_TYPE in error_iter.__next__()
    assert errors.DURATION_LIMIT_WITHOUT_LIMIT_TYPE in error_iter.__next__()
    assert errors.INVALID_DURATION_LIMIT in error_iter.__next__()
    assert errors.DURATION_LIMIT_TYPE_WITHOUT_DURATION in error_iter.__next__()

    # check amounts
    assert errors.INVALID_FARE_TRANSFER_TYPE in error_iter.__next__()

    # check linked entities
    assert errors.NONEXISTENT_FARE_PRODUCT_ID in error_iter.__next__()

    try:
        should_not_exist = error_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True


def test_required_fields():
    results = run_validator(test_data_dir / 'required_fields_test', False)
    error_iter = results.errors.__iter__()

    area_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in area_error
    assert 'areas.txt' in area_error

    stop_area_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in stop_area_error
    assert 'stop_areas.txt' in stop_area_error

    calendar_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in calendar_error
    assert 'calendar.txt' in calendar_error

    calendar_dates_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in calendar_dates_error
    assert 'calendar_dates.txt' in calendar_dates_error

    timeframes_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in timeframes_error
    assert 'timeframes.txt' in timeframes_error

    rider_categories_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in rider_categories_error
    assert 'rider_categories.txt' in rider_categories_error

    fare_containers_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in fare_containers_error
    assert 'fare_containers.txt' in fare_containers_error

    fare_products_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in fare_products_error
    assert 'fare_products.txt' in fare_products_error

    fare_leg_rules_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in fare_leg_rules_error
    assert 'fare_leg_rules.txt' in fare_leg_rules_error

    fare_transfer_rules_error = error_iter.__next__()
    assert errors.REQUIRED_FIELD_MISSING in fare_transfer_rules_error
    assert 'fare_transfer_rules.txt' in fare_transfer_rules_error

    try:
        should_not_exist = error_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True
