from run_validator import run_validator
from src import warnings
from os import path

def test_warnings():
    results = run_validator(path.join('tests', 'test_data', 'warnings_test_gtfs'), True)
    warnings_list = results['warnings']

    print(warnings_list)

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