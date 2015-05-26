from raygun4py import raygunmsgs


def ignore_exceptions(ignoredExceptions, message):
    if message.get_error().get_classname() in ignoredExceptions:
        return None

    return message


def filter_keys(filteredKeys, object):
    iterationTarget = object

    if isinstance(object, raygunmsgs.RaygunMessage):
        iterationTarget = object.__dict__

    for key in iterationTarget.iterkeys():
        if key in filteredKeys:
            iterationTarget[key] = '<filtered>'

        elif isinstance(iterationTarget[key], dict):
            iterationTarget[key] = filter_keys(filteredKeys, iterationTarget[key])

    return iterationTarget


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
