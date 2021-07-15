from run_validator import run_validator
from os import path

def test_errors_simple_files():
    results = run_validator(path.join('tests', 'test_data', 'bad_gtfs_simple'), True)
    errors = results['errors']
    
    # Areas errors
    assert 'defined twice' in errors[0]
    assert 'has empty area id' in errors[1]
    assert 'has itself' in errors[2]

    # Stops errors
    assert 'references an area_id that does not exist' in errors[5]

    # Stop times errors
    assert 'references an area_id that does not exist' in errors[6]

    # Calendar errors
    assert 'includes a line with an empty service_id' in errors[7]
    assert 'the same service_id' in errors[8]
    
    # Calendar dates errors
    assert 'includes a line with an empty service_id' in errors[9]

    # Timeframes errors
    assert 'has an invalid time format' in errors[10]
    assert 'has an invalid time format' in errors[11]
    assert 'empty start_time' in errors[12]
    assert 'empty end_time' in errors[13]
    assert 'empty timeframe_id' in errors[14]

    # Rider categories errors
    assert 'has an empty rider_category_id' in errors[15]
    assert 'has a negative min_age' in errors[16]
    assert 'has a negative max_age' in errors[17]
    assert 'has a non-integer min_age' in errors[18]
    assert 'has a non-integer max_age' in errors[19]

    # Fare containers errors
    assert 'does not have a fare_container_id' in errors[20]
    assert 'does not have a fare_container_name' in errors[21]
    assert 'is not defined in rider_categories' in errors[22]
    assert 'has been defined without a currency' in errors[23]
    assert 'defined, but is not an integer or float' in errors[24]
    assert 'has been defined without a currency' in errors[25]
    assert 'defined, but is not an integer or float' in errors[26]
    assert 'defined without an amount' in errors[27]
    assert 'is defined twice in fare_containers' in errors[28]

    assert len(errors) == 29

def test_errors_fare_products():
    results = run_validator(path.join('tests', 'test_data', 'bad_fare_products'), True)
    errors = results['errors']

    # Fare products errors
    assert 'has an empty fare_product_id' in errors[0]
    assert 'has an empty fare_product_name' in errors[1]
    assert 'min_ or max_amount defined without its counterpart' in errors[2]
    assert 'amount and at least one of min_ or max_amount defined' in errors[3]
    assert 'has been defined without a currency' in errors[4]
    assert 'has been defined without a currency' in errors[5]
    assert 'has been defined without a currency' in errors[6] # this also is for line 7 of fare products
    assert 'has no amount, min_amount, or max_amount' in errors[7]
    assert 'is referenced, but it does not exist' in errors[8]
    assert 'has an invalid value, or is required and does not exist' in errors[9]
    assert 'has an invalid value, or is required and does not exist' in errors[10]
    assert 'is referenced, but it does not exist' in errors[11]
    assert 'referenced without an accompanying timeframe_id' in errors[12]

    assert len(errors) == 13
