import jsonpickle

def ignore_exceptions(ignoredExceptions, message):
    if message.get_error().get_classname() in ignoredExceptions:
        return None

    return message


def filter_keys(filteredKeys, message):
    return message


def set_proxy():
    pass
