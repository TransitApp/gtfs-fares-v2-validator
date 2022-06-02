from .errors import *


def check_leg_groups(line, leg_group_ids, unused_leg_groups):
    if line.from_leg_group_id and line.from_leg_group_id not in leg_group_ids:
        line.add_error(INVALID_FROM_LEG_GROUP)
    if line.to_leg_group_id and line.to_leg_group_id not in leg_group_ids:
        line.add_error(INVALID_TO_LEG_GROUP)

    if line.from_leg_group_id in unused_leg_groups:
        unused_leg_groups.remove(line.from_leg_group_id)
    if line.to_leg_group_id in unused_leg_groups:
        unused_leg_groups.remove(line.to_leg_group_id)


def check_transfer_count(line):
    if line.transfer_count:
        if line.from_leg_group_id != line.to_leg_group_id:
            line.add_error(TRANSFER_COUNT_WITH_BAD_LEGS)
        try:
            limit = int(line.transfer_count)
            if limit < 1 and limit != -1:
                line.add_error(INVALID_TRANSFER_COUNT)
        except ValueError:
            line.add_error(INVALID_TRANSFER_COUNT)


def check_durations(line):
    if line.duration_limit_type and line.duration_limit_type not in {
            '0', '1', '2', '3'
    }:
        line.add_error(INVALID_DURATION_LIMIT_TYPE)

    if line.duration_limit:
        if not line.duration_limit_type:
            line.add_error(DURATION_LIMIT_WITHOUT_LIMIT_TYPE)
        try:
            limit = int(line.duration_limit)
            if limit < 1:
                line.add_error(INVALID_DURATION_LIMIT)
        except ValueError:
            line.add_error(INVALID_DURATION_LIMIT)
    else:
        if line.duration_limit_type:
            line.add_error(DURATION_LIMIT_TYPE_WITHOUT_DURATION)
