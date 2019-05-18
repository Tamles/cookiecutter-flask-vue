from functools import partial
import arrow


def non_empty(value, field_type):
    if field_type == 'str':
        value = str(value)
    elif field_type == 'int':
        value = int(value)
    elif field_type == 'datetime':
        value = arrow.get(value).naive
    if not value:
        raise ValueError('Must not be empty value')
    return value


non_empty_str = partial(non_empty, field_type='str')
non_empty_datetime = partial(non_empty, field_type='datetime')
non_empty_int = partial(non_empty, field_type='int')
