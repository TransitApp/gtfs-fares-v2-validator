from fares_validator.loader import run_validator
from fares_validator import warnings
from pathlib import Path

test_data_dir = Path(__file__).parent / 'test_data'

def test_warnings():
    results = run_validator(test_data_dir / 'warnings_test_gtfs', True)

    # Stops / stop times warnings
    assert warnings.UNUSED_AREAS_IN_STOPS in results.warnings[0]

    # Rider categories warnings
    assert warnings.MAX_AGE_LESS_THAN_MIN_AGE in results.warnings[1]
    assert warnings.VERY_LARGE_MIN_AGE in results.warnings[2]
    assert warnings.VERY_LARGE_MAX_AGE in results.warnings[3]

    # Fare products warnings
    assert warnings.OFFSET_AMOUNT_WITHOUT_OFFSET_UNIT in results.warnings[4]

    # Fare leg rule warnings
    assert warnings.UNUSED_AREA_IDS in results.warnings[5]
    assert warnings.UNUSED_NETWORK_IDS in results.warnings[6]

    # Fare transfer rule warnings
    assert warnings.UNUSED_LEG_GROUPS in results.warnings[7]

    # generic warnings
    assert warnings.UNUSED_TIMEFRAME_IDS in results.warnings[8]

    assert len(results.warnings) == 9

def test_warnings_nonexistent_files():
    results = run_validator(test_data_dir / 'no_files', True)

    assert warnings.NO_AREAS in results.warnings[0]
    assert warnings.NO_ROUTES in results.warnings[1]
    assert warnings.NO_STOPS in results.warnings[2]
    assert warnings.NO_SERVICE_IDS in results.warnings[3]
    assert warnings.NO_TIMEFRAMES in results.warnings[4]
    assert warnings.NO_RIDER_CATEGORIES in results.warnings[5]
    assert warnings.NO_FARE_CONTAINERS in results.warnings[6]
    assert warnings.NO_FARE_PRODUCTS in results.warnings[7]
    assert warnings.NO_FARE_LEG_RULES in results.warnings[8]
    assert warnings.NO_FARE_TRANSFER_RULES in results.warnings[9]

    assert len(results.warnings) == 10
