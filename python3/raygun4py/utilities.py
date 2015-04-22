import jsonpickle
from raygun4py import raygunmsgs


def ignore_exceptions(ignoredExceptions, message):
    if message.get_error().get_classname() in ignoredExceptions:
        return None

    return message


def filter_keys(filteredKeys, object):
    iterationTarget = object

    if isinstance(object, raygunmsgs.RaygunMessage):
        iterationTarget = object.__dict__

    for key in iter(iterationTarget.keys()):
        if key in filteredKeys:
            iterationTarget[key] = '<filtered>'

        elif isinstance(iterationTarget[key], dict):
            iterationTarget[key] = filter_keys(filteredKeys, iterationTarget[key])

    return iterationTarget
