from .errors import *

def check_leg_groups(line, line_num_error_msg, leg_group_ids, unused_leg_groups, messages):
    from_leg_group = line.get('from_leg_group_id')
    to_leg_group = line.get('to_leg_group_id')
    is_symmetrical = line.get('is_symmetrical')

    if is_symmetrical and is_symmetrical not in {'0', '1'}:
        messages.add_error(INVALID_IS_SYMMETRICAL_TRANSFER_RULES, line_num_error_msg)
    if (from_leg_group or to_leg_group) and not is_symmetrical:
        messages.add_error(LEG_GROUP_WITHOUT_IS_SYMMETRICAL, line_num_error_msg)
    if (not from_leg_group and not to_leg_group) and is_symmetrical:
        messages.add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_LEG_GROUP, line_num_error_msg)
    if from_leg_group and not from_leg_group in leg_group_ids:
        messages.add_error(INVALID_FROM_LEG_GROUP, line_num_error_msg)       
    if to_leg_group and not to_leg_group in leg_group_ids:
        messages.add_error(INVALID_TO_LEG_GROUP, line_num_error_msg)

    if from_leg_group in unused_leg_groups:
        unused_leg_groups.remove(from_leg_group)
    if to_leg_group in unused_leg_groups:
        unused_leg_groups.remove(to_leg_group)

def check_spans_and_transfer_ids(line, line_num_error_msg, messages):
    spanning_limit = line.get('spanning_limit')
    transfer_id = line.get('transfer_id')
    transfer_seq = line.get('transfer_sequence')

    if spanning_limit:
        if line.get('from_leg_group_id') != line.get('to_leg_group_id'):
            messages.add_error(SPANNING_LIMIT_WITH_BAD_LEGS, line_num_error_msg)
        if transfer_id:
            messages.add_error(SPANNING_LIMIT_WITH_TRANSFER_ID, line_num_error_msg)
        try:
            limit = int(spanning_limit)
            if limit <= 1:
                messages.add_error(INVALID_SPANNING_LIMIT, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_SPANNING_LIMIT, line_num_error_msg)
    
    if transfer_id:
        if not transfer_seq:
            messages.add_error(TRANSFER_ID_WITHOUT_TRANSFER_SEQUENCE, line_num_error_msg)
    
    if transfer_seq:
        if not transfer_id:
            messages.add_error(TRANSFER_SEQUENCE_WITHOUT_TRANSFER_ID, line_num_error_msg)
        try:
            seq = int(transfer_seq)
            if seq < 1:
                messages.add_error(INVALID_TRANSFER_SEQUENCE, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_TRANSFER_SEQUENCE, line_num_error_msg)

def check_durations(line, line_num_error_msg, messages):
    duration_limit = line.get('duration_limit')
    limit_type = line.get('duration_limit_type')

    if limit_type and limit_type not in {'0', '1', '2', '3'}:
        messages.add_error(INVALID_DURATION_LIMIT_TYPE, line_num_error_msg)

    if duration_limit:
        if not limit_type:
            messages.add_error(DURATION_LIMIT_WITHOUT_LIMIT_TYPE, line_num_error_msg)
        try:
            limit = int(duration_limit)
            if limit < 1:
                add_error(INVALID_DURATION_LIMIT, line_num_error_msg)
        except ValueError:
            messages.add_error(INVALID_DURATION_LIMIT, line_num_error_msg)
    else:
        if limit_type:
            messages.add_error(DURATION_LIMIT_TYPE_WITHOUT_DURATION, line_num_error_msg)
