def check_leg_groups(line, line_num_error_msg, leg_group_ids, errors):
    from_leg_group = line.get('from_leg_group_id')
    to_leg_group = line.get('to_leg_group_id')
    is_symmetrical = line.get('is_symmetrical')

    if is_symmetrical and (not is_symmetrical in ['0', '1']):
        errors.append('An is_symmetrical in fare_transfer_rules is not one of the accepted values.' + line_num_error_msg)
    
    if (from_leg_group or to_leg_group) and not is_symmetrical:
        errors.append('An is_symmetrical in fare_transfer_rules is not defined, but from or to leg group is.' + line_num_error_msg)
    if (not from_leg_group and not to_leg_group) and is_symmetrical:
        errors.append('An is_symmetrical in fare_transfer_rules is defined, but no from or to leg group is.' + line_num_error_msg)
    
    if from_leg_group and not from_leg_group in leg_group_ids:
        errors.append('A from_leg_group in fare_transfer_rules does not exist.' + line_num_error_msg)
    if to_leg_group and not to_leg_group in leg_group_ids:
        errors.append('A to_leg_group in fare_transfer_rules does not exist.' + line_num_error_msg)

def check_spans_and_transfer_ids(line, line_num_error_msg, errors):
    spanning_limit = line.get('spanning_limit')
    transfer_id = line.get('transfer_id')
    transfer_seq = line.get('transfer_sequence')

    if spanning_limit:
        if not (line.get('from_leg_group_id') == line.get('to_leg_group_id')):
            errors.append('A fare_transfer_rule has spanning_limit with different from and to leg group ids.' + line_num_error_msg)
        if transfer_id:
            errors.append('A fare_transfer_rule has spanning_limit with transfer_id defined.' + line_num_error_msg)
        try:
            limit = int(spanning_limit)
            if limit < 0 or limit == 1:
                errors.append('A fare_transfer_rule has spanning_limit with invalid integer.' + line_num_error_msg)
        except ValueError:
            errors.append('A fare_transfer_rule has spanning_limit with incorrect type.' + line_num_error_msg)
    
    if transfer_id:
        if not transfer_seq:
            errors.append('A transfer_id is defined without a transfer_sequence.' + line_num_error_msg)
    
    if transfer_seq:
        if not transfer_id:
            errors.append('A transfer_sequence is defined without a transfer_id.' + line_num_error_msg)
        try:
            seq = int(transfer_seq)
            if seq < 1:
                errors.append('A fare_transfer_rule has transfer_sequence with invalid integer.' + line_num_error_msg)
        except ValueError:
            errors.append('A fare_transfer_rule has transfer_sequence with incorrect type.' + line_num_error_msg)

def check_durations(line, line_num_error_msg, errors):
    duration_limit = line.get('duration_limit')
    limit_type = line.get('duration_limit_type')

    if limit_type and (not limit_type in ['0', '1', '2', '3']):
        errors.append('A fare_transfer_rule has duration_limit_type with invalid value.' + line_num_error_msg)

    if duration_limit:
        if not limit_type:
            errors.append('A fare_transfer_rule has duration_limit without duration_limit_type.' + line_num_error_msg)
        try:
            limit = int(duration_limit)
            if limit < 1:
                errors.append('A fare_transfer_rule has duration_limit with invalid integer.' + line_num_error_msg)
        except ValueError:
            errors.append('A fare_transfer_rule has duration_limit with incorrect type.' + line_num_error_msg)
    else:
        if limit_type:
            errors.append('A fare_transfer_rule has duration_limit_type without duration_limit.' + line_num_error_msg)