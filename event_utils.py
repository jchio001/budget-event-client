required_fields_dict = {
    'client_id': 'cid',
    'local_id': 'local_id',
    'event_category': 'ec',
    'event_action': 'ea',
    'creation_time': 'creation_time'
}


def get_missing_fields_for_event(event):
    missing_fields = []

    for field in required_fields_dict.keys():
        if not event.get(field):
            missing_fields.append(field)

    return missing_fields
