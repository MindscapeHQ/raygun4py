from raygun4py import raygunmsgs


def ignore_exceptions(ignored_exceptions, message):
    if message.get_error().get_classname() in ignored_exceptions:
        return None

    return message


def filter_keys(filtered_keys, object):
    iteration_target = object

    if isinstance(object, raygunmsgs.RaygunMessage):
        iteration_target = object.__dict__

    for key in iteration_target.iterkeys():
        if key in filtered_keys:
            iteration_target[key] = '<filtered>'

        elif isinstance(iteration_target[key], dict):
            iteration_target[key] = filter_keys(filtered_keys, iteration_target[key])

    return iteration_target


def execute_grouping_key(grouping_key_callback, message):
    if grouping_key_callback is not None:
        grouping_key = grouping_key_callback(message)

        if grouping_key is not None and isinstance(grouping_key, str) and 0 < len(grouping_key) <= 100:
            return grouping_key

    return None


def camel(k):
    "Turns snake_case_strings into camelCaseStrings."
    if k.lower() != k:
        return k  # Don't transform camelCase value, it's good to go.
    new_key = k.replace('_', ' ').title().replace(' ', '')
    return new_key[0].lower() + new_key[1:]


def camelize_dict(d):
    return dict([
        (camel(k), v) for k, v in d.items()
    ])
