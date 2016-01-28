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
