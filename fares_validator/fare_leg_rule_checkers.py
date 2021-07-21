from .utils import check_linked_id
from .errors import *

def check_areas(path, line, line_num_error_msg, areas, unused_areas, messages):
    is_symmetrical = line.get('is_symmetrical')
    if is_symmetrical and is_symmetrical not in {'0', '1'}:
        messages.add_error(INVALID_IS_SYMMETRICAL_LEG_RULES, line_num_error_msg)
    
    from_area = line.get('from_area_id')
    to_area = line.get('to_area_id')
    contains_area = line.get('contains_area_id')

    if contains_area and (not from_area and not to_area):
        messages.add_error(CONTAINS_AREA_WITHOUT_FROM_TO_AREA, line_num_error_msg)
    
    if (from_area or to_area) and not is_symmetrical:
        messages.add_error(AREA_WITHOUT_IS_SYMMETRICAL, line_num_error_msg)
    
    if (not from_area and not to_area) and is_symmetrical:
        messages.add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_AREA, line_num_error_msg)
    
    if from_area and from_area in unused_areas:
        unused_areas.remove(from_area)
    if to_area and to_area in unused_areas:
        unused_areas.remove(from_area)

    check_linked_id(path, line, 'from_area_id', areas, line_num_error_msg, messages)
    check_linked_id(path, line, 'to_area_id', areas, line_num_error_msg, messages)
    check_linked_id(path, line, 'contains_area_id', areas, line_num_error_msg, messages)

def check_distances(line, line_num_error_msg, messages):
    min_distance = line.get('min_distance')
    max_distance = line.get('max_distance')
    distance_type = line.get('distance_type')
    
    if distance_type and distance_type not in {'0', '1'}:
        messages.add_error(INVALID_DISTANCE_TYPE, line_num_error_msg)

    if min_distance:
        try:
            dist = float(min_distance)
            if dist < 0:
                messages.add_error(NEGATIVE_MIN_DISTANCE, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_MIN_DISTANCE, line_num_error_msg)
    if max_distance:
        try:
            dist = float(max_distance)
            if dist < 0:
               messages.add_error(NEGATIVE_MAX_DISTANCE, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_MAX_DISTANCE, line_num_error_msg)
    
    if (min_distance or max_distance) and not distance_type:
        messages.add_error(DISTANCE_WITHOUT_DISTANCE_TYPE, line_num_error_msg)
    if (not min_distance and not max_distance) and distance_type:
        messages.add_error(DISTANCE_TYPE_WITHOUT_DISTANCE, line_num_error_msg)