from fares_validator.utils import check_area_cycles
from fares_validator import diagnostics, errors

def test_area_cycles():
    messages = diagnostics.Diagnostics()

    min_cycle = {
        '1': ['1']
    }
    check_area_cycles(min_cycle, messages)
    assert errors.GREATER_AREA_ID_LOOP in messages.errors[0]
    assert len(messages.errors) == 1
    
    not_a_cycle = {
        '2': ['1'],
        '3': ['4'],
        '4': ['5'],
        '1': [],
        '5': ['2']
    }
    check_area_cycles(not_a_cycle, messages)
    assert len(messages.errors) == 1

    more_complex_not_a_cycle = {
        '1': ['2', '3', '4'],
        '2': [],
        '3': ['2'],
        '4': ['3']
    }
    check_area_cycles(more_complex_not_a_cycle, messages)
    assert len(messages.errors) == 1

    more_complex_cycle = {
        '1': ['2', '3'],
        '2': ['4'],
        '3': ['2'],
        '4': ['3']
    }
    check_area_cycles(more_complex_cycle, messages)
    assert errors.GREATER_AREA_ID_LOOP in messages.errors[1]
    assert len(messages.errors) == 2

