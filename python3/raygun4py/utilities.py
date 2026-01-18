from __future__ import annotations

import re
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from raygun4py import raygunmsgs


def ignore_exceptions(
    ignored_exceptions: list[type[Exception]],
    message: raygunmsgs.RaygunMessage,
) -> raygunmsgs.RaygunMessage | None:
    error = message.get_error()
    if error is None:
        return message
    classname = error.get_classname()
    if classname and classname in [e.__name__ for e in ignored_exceptions]:
        return None

    return message


def filter_keys(filtered_keys: list[str], obj: dict[str, Any]) -> dict[str, Any]:
    """
    Filter keys from a dictionary.

    Parameters:
        filtered_keys (list): A list of keys to filter.
        obj (dict): The dictionary to filter.

    Returns:
        dict: The filtered dictionary.
    """
    iteration_target = dict(obj)

    for key in iter(iteration_target.keys()):
        if isinstance(iteration_target[key], dict):
            iteration_target[key] = filter_keys(filtered_keys, iteration_target[key])
        else:
            for filter_key in filtered_keys:
                # Wildcard matching
                if "*" in filter_key:
                    filter_key_sanitised = filter_key.replace("*", "")
                    # `*foo*` Match any key that contains the filter key
                    if filter_key.startswith("*") and filter_key.endswith("*"):
                        if filter_key_sanitised in key:
                            iteration_target[key] = "<filtered>"
                    # `*foo` Match any key that ends with the filter key
                    elif filter_key.startswith("*") and key.endswith(
                        filter_key_sanitised
                    ):
                        iteration_target[key] = "<filtered>"
                    # `foo*` Match any key that starts with the filter key
                    elif filter_key.endswith("*") and key.startswith(
                        filter_key_sanitised
                    ):
                        iteration_target[key] = "<filtered>"
                # Exact matching
                elif filter_key == key:
                    iteration_target[key] = "<filtered>"

    return iteration_target


def execute_grouping_key(
    grouping_key_callback: Callable[[raygunmsgs.RaygunMessage], str] | None,
    message: raygunmsgs.RaygunMessage,
) -> str | None:
    if grouping_key_callback is not None:
        grouping_key = grouping_key_callback(message)

        if (
            grouping_key is not None
            and isinstance(grouping_key, str)
            and 0 < len(grouping_key) <= 100
        ):
            return grouping_key

    return None


def camelcase_to_snakecase(key: str) -> str:
    "Turns camelCaseStrings into snake_case_strings."
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snakecase_dict(d: dict[str, Any]) -> dict[str, Any]:
    return dict([(camelcase_to_snakecase(k), v) for k, v in d.items()])
