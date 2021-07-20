from fares_validator.loader import run_validator
from fares_validator import warnings
from pathlib import Path

test_data_dir = Path(__file__).parent / 'test_data'

def test_warnings():
    results = run_validator(test_data_dir / 'warnings_test_gtfs', True)
    warnings_list = results['warnings']

    # Stops / stop times warnings
    assert warnings.UNUSED_AREAS_IN_STOPS in warnings_list[0]

    # Rider categories warnings
    assert warnings.MAX_AGE_LESS_THAN_MIN_AGE in warnings_list[1]
    assert warnings.VERY_LARGE_MIN_AGE in warnings_list[2]
    assert warnings.VERY_LARGE_MAX_AGE in warnings_list[3]

    # Fare products warnings
    assert warnings.OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT in warnings_list[4]

    # Fare leg rule warnings
    assert warnings.UNUSED_AREA_IDS in warnings_list[5]
    assert warnings.UNUSED_NETWORK_IDS in warnings_list[6]

    # Fare transfer rule warnings
    assert warnings.UNUSED_LEG_GROUPS in warnings_list[7]

    # generic warnings
    assert warnings.UNUSED_TIMEFRAME_IDS in warnings_list[8]

    assert len(warnings_list) == 9

def test_warnings_nonexistent_files():
    results = run_validator(test_data_dir / 'no_files', True)
    warnings_list = results['warnings']

    assert warnings.NO_AREAS in warnings_list[0]
    assert warnings.NO_ROUTES in warnings_list[1]
    assert warnings.NO_STOPS in warnings_list[2]
    assert warnings.NO_SERVICE_IDS in warnings_list[3]
    assert warnings.NO_TIMEFRAMES in warnings_list[4]
    assert warnings.NO_RIDER_CATEGORIES in warnings_list[5]
    assert warnings.NO_FARE_CONTAINERS in warnings_list[6]
    assert warnings.NO_FARE_PRODUCTS in warnings_list[7]
    assert warnings.NO_FARE_LEG_RULES in warnings_list[8]
    assert warnings.NO_FARE_TRANSFER_RULES in warnings_list[9]

    assert len(warnings_list) == 10
