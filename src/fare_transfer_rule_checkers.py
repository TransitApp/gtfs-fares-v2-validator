from .errors import *

def check_leg_groups(line, line_num_error_msg, leg_group_ids, errors):
    from_leg_group = line.get('from_leg_group_id')
    to_leg_group = line.get('to_leg_group_id')
    is_symmetrical = line.get('is_symmetrical')

    if is_symmetrical and (not is_symmetrical in ['0', '1']):
        add_error(INVALID_IS_SYMMETRICAL_TRANSFER_RULES, line_num_error_msg, errors)
    if (from_leg_group or to_leg_group) and not is_symmetrical:
        add_error(LEG_GROUP_WITHOUT_IS_SYMMETRICAL, line_num_error_msg, errors)
    if (not from_leg_group and not to_leg_group) and is_symmetrical:
        add_error(IS_SYMMETRICAL_WITHOUT_FROM_TO_LEG_GROUP, line_num_error_msg, errors)
    if from_leg_group and not from_leg_group in leg_group_ids:
        add_error(INVALID_FROM_LEG_GROUP, line_num_error_msg, errors)
    if to_leg_group and not to_leg_group in leg_group_ids:
        add_error(INVALID_TO_LEG_GROUP, line_num_error_msg, errors)

def check_spans_and_transfer_ids(line, line_num_error_msg, errors):
    spanning_limit = line.get('spanning_limit')
    transfer_id = line.get('transfer_id')
    transfer_seq = line.get('transfer_sequence')

    if spanning_limit:
        if not (line.get('from_leg_group_id') == line.get('to_leg_group_id')):
            add_error(SPANNING_LIMIT_WITH_BAD_LEGS, line_num_error_msg, errors)
        if transfer_id:
            add_error(SPANNING_LIMIT_WITH_TRANSFER_ID, line_num_error_msg, errors)
        try:
            limit = int(spanning_limit)
            if limit < 0 or limit == 1:
                add_error(INVALID_SPANNING_LIMIT, line_num_error_msg, errors)
        except ValueError:
            add_error(INVALID_SPANNING_LIMIT + line_num_error_msg, errors)
    
    if transfer_id:
        if not transfer_seq:
            add_error(TRANSFER_ID_WITHOUT_TRANSFER_SEQUENCE, line_num_error_msg, errors)
    
    if transfer_seq:
        if not transfer_id:
            add_error(TRANSFER_SEQUENCE_WITHOUT_TRANSFER_ID, line_num_error_msg, errors)
        try:
            seq = int(transfer_seq)
            if seq < 1:
                add_error(INVALID_TRANSFER_SEQUENCE, line_num_error_msg, errors)
        except ValueError:
            add_error(INVALID_TRANSFER_SEQUENCE, line_num_error_msg, errors)

def check_durations(line, line_num_error_msg, errors):
    duration_limit = line.get('duration_limit')
    limit_type = line.get('duration_limit_type')

    if limit_type and (not limit_type in ['0', '1', '2', '3']):
        add_error(INVALID_DURATION_LIMIT_TYPE, line_num_error_msg, errors)

    if duration_limit:
        if not limit_type:
            add_error(DURATION_LIMIT_WITHOUT_LIMIT_TYPE, line_num_error_msg, errors)
        try:
            limit = int(duration_limit)
            if limit < 1:
                add_error(INVALID_DURATION_LIMIT, line_num_error_msg, errors)
        except ValueError:
            add_error(INVALID_DURATION_LIMIT, line_num_error_msg, errors)
    else:
        if limit_type:
            add_error(DURATION_LIMIT_TYPE_WITHOUT_DURATION, line_num_error_msg, errors)