from fares_validator.loader import run_validator
from fares_validator import warnings
from pathlib import Path

test_data_dir = Path(__file__).parent / 'test_data'


def test_warnings():
    results = run_validator(test_data_dir / 'warnings_test_gtfs')
    warning_iter = results.warnings.__iter__()

    # Rider categories warnings
    assert warnings.MAX_AGE_LESS_THAN_MIN_AGE in warning_iter.__next__()
    assert warnings.VERY_LARGE_MIN_AGE in warning_iter.__next__()
    assert warnings.VERY_LARGE_MAX_AGE in warning_iter.__next__()

    # Fare products warnings
    assert warnings.OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT in warning_iter.__next__()

    # Fare leg rule warnings
    assert warnings.UNUSED_AREA_IDS in warning_iter.__next__()
    assert warnings.UNUSED_NETWORK_IDS in warning_iter.__next__()

    # Fare transfer rule warnings
    assert warnings.UNUSED_LEG_GROUPS in warning_iter.__next__()

    # generic warnings
    assert warnings.UNUSED_TIMEFRAME_IDS in warning_iter.__next__()

    try:
        should_not_exist = warning_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True


def test_warnings_nonexistent_files():
    results = run_validator(test_data_dir / 'no_files')
    warning_iter = results.warnings.__iter__()

    assert warnings.NO_AREAS in warning_iter.__next__()
    assert warnings.NO_STOPS in warning_iter.__next__()
    assert warnings.NO_STOP_AREAS in warning_iter.__next__()
    assert warnings.NO_ROUTES in warning_iter.__next__()
    assert warnings.NO_SERVICE_IDS in warning_iter.__next__()
    assert warnings.NO_TIMEFRAMES in warning_iter.__next__()
    assert warnings.NO_RIDER_CATEGORIES in warning_iter.__next__()
    assert warnings.NO_FARE_CONTAINERS in warning_iter.__next__()
    assert warnings.NO_FARE_PRODUCTS in warning_iter.__next__()
    assert warnings.NO_FARE_LEG_RULES in warning_iter.__next__()
    assert warnings.NO_FARE_TRANSFER_RULES in warning_iter.__next__()

    try:
        should_not_exist = warning_iter.__next__()
        assert not should_not_exist
    except StopIteration:
        assert True
