from .errors import *

def check_leg_groups(line, leg_group_ids, unused_leg_groups, messages):
    if line.is_symmetrical and line.is_symmetrical not in {'0', '1'}:
        messages.add_error(INVALID_IS_SYMMETRICAL_TRANSFER_RULES, line.line_num_error_msg)
    if (line.from_leg_group_id or line.to_leg_group_id) and not line.is_symmetrical:
        messages.add_error(LEG_GROUP_WITHOUT_IS_SYMMETRICAL, line.line_num_error_msg)
    if (not line.from_leg_group_id and not line.to_leg_group_id) and line.is_symmetrical:
        messages.add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_LEG_GROUP, line.line_num_error_msg)
    if line.from_leg_group_id and not line.from_leg_group_id in leg_group_ids:
        messages.add_error(INVALID_FROM_LEG_GROUP, line.line_num_error_msg)
    if line.to_leg_group_id and not line.to_leg_group_id in leg_group_ids:
        messages.add_error(INVALID_TO_LEG_GROUP, line.line_num_error_msg)

    if line.from_leg_group_id in unused_leg_groups:
        unused_leg_groups.remove(line.from_leg_group_id)
    if line.to_leg_group_id in unused_leg_groups:
        unused_leg_groups.remove(line.to_leg_group_id)

def check_spans_and_transfer_ids(line, messages):
    if line.spanning_limit:
        if line.from_leg_group_id != line.to_leg_group_id:
            messages.add_error(SPANNING_LIMIT_WITH_BAD_LEGS, line.line_num_error_msg)
        if line.transfer_id:
            messages.add_error(SPANNING_LIMIT_WITH_TRANSFER_ID, line.line_num_error_msg)
        try:
            limit = int(line.spanning_limit)
            if limit <= 1:
                messages.add_error(INVALID_SPANNING_LIMIT, line.line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_SPANNING_LIMIT, line.line_num_error_msg)

    if line.transfer_id:
        if not line.transfer_sequence:
            messages.add_error(TRANSFER_ID_WITHOUT_TRANSFER_SEQUENCE, line.line_num_error_msg)

    if line.transfer_sequence:
        if not line.transfer_id:
            messages.add_error(TRANSFER_SEQUENCE_WITHOUT_TRANSFER_ID, line.line_num_error_msg)
        try:
            seq = int(line.transfer_sequence)
            if seq < 1:
                messages.add_error(INVALID_TRANSFER_SEQUENCE, line.line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_TRANSFER_SEQUENCE, line.line_num_error_msg)

def check_durations(line, messages):
    if line.duration_limit_type and line.duration_limit_type not in {'0', '1', '2', '3'}:
        messages.add_error(INVALID_DURATION_LIMIT_TYPE, line.line_num_error_msg)

    if line.duration_limit:
        if not line.duration_limit_type:
            messages.add_error(DURATION_LIMIT_WITHOUT_LIMIT_TYPE, line.line_num_error_msg)
        try:
            limit = int(line.duration_limit)
            if limit < 1:
                messages.add_error(INVALID_DURATION_LIMIT, line.line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_DURATION_LIMIT, line.line_num_error_msg)
    else:
        if line.duration_limit_type:
            messages.add_error(DURATION_LIMIT_TYPE_WITHOUT_DURATION, line.line_num_error_msg)
