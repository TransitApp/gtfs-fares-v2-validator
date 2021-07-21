from .errors import *
from . import utils


def check_areas(line, areas, unused_areas):
    if line.is_symmetrical and line.is_symmetrical not in {'0', '1'}:
        line.add_error(INVALID_IS_SYMMETRICAL_LEG_RULES)

    if line.contains_area_id and (not line.from_area_id and not line.to_area_id):
        line.add_error(CONTAINS_AREA_WITHOUT_FROM_TO_AREA)

    if (line.from_area_id or line.to_area_id) and not line.is_symmetrical:
        line.add_error(AREA_WITHOUT_IS_SYMMETRICAL)

    if (not line.from_area_id and not line.to_area_id) and line.is_symmetrical:
        line.add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_AREA)

    if line.from_area_id and line.from_area_id in unused_areas:
        unused_areas.remove(line.from_area_id)
    if line.to_area_id and line.to_area_id in unused_areas:
        unused_areas.remove(line.from_area_id)

    utils.check_linked_id(line, 'from_area_id', areas)
    utils.check_linked_id(line, 'to_area_id', areas)
    utils.check_linked_id(line, 'contains_area_id', areas)


def check_distances(line):
    if line.distance_type and line.distance_type not in {'0', '1'}:
        line.add_error(INVALID_DISTANCE_TYPE)

    if line.min_distance:
        try:
            dist = float(line.min_distance)
            if dist < 0:
                line.add_error(NEGATIVE_MIN_DISTANCE)
        except ValueError:
            line.add_error(INVALID_MIN_DISTANCE)
    if line.max_distance:
        try:
            dist = float(line.max_distance)
            if dist < 0:
                line.add_error(NEGATIVE_MAX_DISTANCE)
        except ValueError:
            line.add_error(INVALID_MAX_DISTANCE)

    if (line.min_distance or line.max_distance) and not line.distance_type:
        line.add_error(DISTANCE_WITHOUT_DISTANCE_TYPE)
    if (not line.min_distance and not line.max_distance) and line.distance_type:
        line.add_error(DISTANCE_TYPE_WITHOUT_DISTANCE)
