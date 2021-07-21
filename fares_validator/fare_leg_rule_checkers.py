from .utils import check_linked_id
from .errors import *

def check_areas(path, line, line_num_error_msg, areas, unused_areas, messages):
    if line.is_symmetrical and line.is_symmetrical not in {'0', '1'}:
        messages.add_error(INVALID_IS_SYMMETRICAL_LEG_RULES, line_num_error_msg)

    if line.contains_area_id and (not line.from_area_id and not line.to_area_id):
        messages.add_error(CONTAINS_AREA_WITHOUT_FROM_TO_AREA, line_num_error_msg)
    
    if (line.from_area_id or line.to_area_id) and not line.is_symmetrical:
        messages.add_error(AREA_WITHOUT_IS_SYMMETRICAL, line_num_error_msg)
    
    if (not line.from_area_id and not line.to_area_id) and line.is_symmetrical:
        messages.add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_AREA, line_num_error_msg)
    
    if line.from_area_id and line.from_area_id in unused_areas:
        unused_areas.remove(line.from_area_id)
    if line.to_area_id and line.to_area_id in unused_areas:
        unused_areas.remove(line.from_area_id)

    check_linked_id(path, line, 'from_area_id', areas, line_num_error_msg, messages)
    check_linked_id(path, line, 'to_area_id', areas, line_num_error_msg, messages)
    check_linked_id(path, line, 'contains_area_id', areas, line_num_error_msg, messages)

def check_distances(line, line_num_error_msg, messages):
    if line.distance_type and line.distance_type not in {'0', '1'}:
        messages.add_error(INVALID_DISTANCE_TYPE, line_num_error_msg)

    if line.min_distance:
        try:
            dist = float(line.min_distance)
            if dist < 0:
                messages.add_error(NEGATIVE_MIN_DISTANCE, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_MIN_DISTANCE, line_num_error_msg)
    if line.max_distance:
        try:
            dist = float(line.max_distance)
            if dist < 0:
               messages.add_error(NEGATIVE_MAX_DISTANCE, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_MAX_DISTANCE, line_num_error_msg)
    
    if (line.min_distance or line.max_distance) and not line.distance_type:
        messages.add_error(DISTANCE_WITHOUT_DISTANCE_TYPE, line_num_error_msg)
    if (not line.min_distance and not line.max_distance) and line.distance_type:
        messages.add_error(DISTANCE_TYPE_WITHOUT_DISTANCE, line_num_error_msg)
