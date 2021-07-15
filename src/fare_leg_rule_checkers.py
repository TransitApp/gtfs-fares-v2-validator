from .utils import check_linked_id

def check_areas(path, line, line_num_error_msg, areas, errors):
    is_symmetrical = line.get('is_symmetrical')
    if is_symmetrical and (not is_symmetrical in ['0', '1']):
        errors.append('An is_symmetrical in fare_leg_rules is not one of the accepted values.' + line_num_error_msg)
    
    from_area = line.get('from_area_id')
    to_area = line.get('to_area_id')
    contains_area = line.get('contains_area_id')

    if contains_area and (not from_area and not to_area):
        errors.append('An contains_area in fare_leg_rules is defined without a from and to area.' + line_num_error_msg)
    
    if (from_area or to_area) and not is_symmetrical:
        errors.append('An from and/or to_ area in fare_leg_rules is defined without is_symmetrical.' + line_num_error_msg)
    
    if (not from_area and not to_area) and is_symmetrical:
        errors.append('An is_symmetrical in fare_leg_rules is defined without a from or to area.' + line_num_error_msg)

    check_linked_id(path, line, 'from_area_id', areas, line_num_error_msg, errors)
    check_linked_id(path, line, 'to_area_id', areas, line_num_error_msg, errors)
    check_linked_id(path, line, 'contains_area_id', areas, line_num_error_msg, errors)

def check_distances(line, line_num_error_msg, errors):
    min_distance = line.get('min_distance')
    max_distance = line.get('max_distance')
    distance_type = line.get('distance_type')
    
    if distance_type and (not distance_type in ['0', '1']):
        errors.append('A distance_type in fare_leg_rules has an invalid value.' + line_num_error_msg)

    if min_distance:
        try:
            dist = float(min_distance)
            if (dist < 0):
                errors.append('A min_distance in fare_leg_rules is smaller than 0.' + line_num_error_msg)
        except ValueError:
            errors.append('A min_distance in fare_leg_rules is not a float.' + line_num_error_msg)
    if max_distance:
        try:
            dist = float(max_distance)
            if (dist < 0):
                errors.append('A max_distance in fare_leg_rules is smaller than 0.' + line_num_error_msg)
        except ValueError:
            errors.append('A max_distance in fare_leg_rules is not a float.' + line_num_error_msg)
    
    if (min_distance or max_distance) and not distance_type:
        errors.append('A min_distance or max_distance in fare_leg_rules is defined without a distance_type.' + line_num_error_msg)
    if (not min_distance and not max_distance) and distance_type:
        errors.append('A distance_type in fare_leg_rules is defined without a min_distance or max_distance.' + line_num_error_msg)