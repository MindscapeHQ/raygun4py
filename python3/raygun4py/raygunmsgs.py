import inspect
import os
import logging
import sys

import jsonpickle

from raygun4py import __version__

try:
    import multiprocessing

    USE_MULTIPROCESSING = True
except ImportError:
    USE_MULTIPROCESSING = False

import platform
from datetime import datetime, timezone

from raygun4py import http_utilities


class RaygunMessageBuilder(object):

    def __init__(self, options):
        self.raygunMessage = RaygunMessage()
        self.options = options

    def new(self):
        return RaygunMessageBuilder(self.options)

    def build(self):
        return self.raygunMessage

    def set_machine_name(self, name):
        self.raygunMessage.details["machineName"] = name
        return self

    def set_environment_details(self, extra_environment_data):
        self.raygunMessage.details["environment"] = {
            "environmentVariables": dict(os.environ),
            "runtimeLocation": sys.executable,
            "runtimeVersion": "Python " + sys.version,
        }

        if self.options.get("transmit_environment_variables", True) is False:
            self.raygunMessage.details["environment"]["environmentVariables"] = None

        # Wrap these so we gracefully fail if we cannot access the system details for any reason
        try:
            self.raygunMessage.details["environment"]["processorCount"] = (
                multiprocessing.cpu_count() if USE_MULTIPROCESSING else "n/a"
            )
        except Exception:  # pragma: no cover
            pass

        try:
            self.raygunMessage.details["environment"][
                "architecture"
            ] = platform.architecture()[0]
        except Exception:  # pragma: no cover
            pass

        try:
            self.raygunMessage.details["environment"]["cpu"] = platform.processor()
        except Exception:  # pragma: no cover
            pass

        try:
            self.raygunMessage.details["environment"]["oSVersion"] = "%s %s" % (
                platform.system(),
                platform.release(),
            )
        except Exception:  # pragma: no cover
            pass

        if extra_environment_data is not None:
            merged = extra_environment_data.copy()
            merged.update(self.raygunMessage.details["environment"])
            self.raygunMessage.details["environment"] = merged

        return self

    def set_exception_details(self, raygunExceptionMessage):
        self.raygunMessage.details["error"] = raygunExceptionMessage
        return self

    def set_client_details(self):
        self.raygunMessage.details["client"] = {
            "name": "raygun4py",
            "version": __version__,
            "clientUrl": "https://github.com/MindscapeHQ/raygun4py",
        }
        return self

    def set_customdata(self, user_custom_data):
        if type(user_custom_data) is dict:
            if not self.raygunMessage.details.get("userCustomData"):
                self.raygunMessage.details["userCustomData"] = dict()
            self.raygunMessage.details["userCustomData"].update(user_custom_data)
        return self

    def set_tags(self, tags):
        if type(tags) is list:
            if not self.raygunMessage.details.get("tags"):
                self.raygunMessage.details["tags"] = []
            self.raygunMessage.details["tags"] += tags
        return self

    def set_request_details(self, request):
        if not request:
            return self

        rg_request_details = http_utilities.build_wsgi_compliant_request(request)
        self.raygunMessage.details["request"] = rg_request_details

        return self

    def set_version(self, version):
        self.raygunMessage.details["version"] = version
        return self

    def set_user(self, user):
        if user is not None:
            self.raygunMessage.details["user"] = user
        return self


class RaygunMessage(object):

    def __init__(self):
        self.occurredOn = datetime.now(timezone.utc)
        self.details = {}

    def __copy__(self):
        new_instance = RaygunMessage()
        new_instance.details = self.details.copy()
        new_instance.occurredOn = self.occurredOn
        return new_instance

    def copy(self):
        return self.__copy__()

    def get_error(self):
        return self.details.get("error")

    def get_details(self):
        return self.details

    def set_details(self, details):
        self.details = details

    def set_error(self, error):
        self.details["error"] = error


class RaygunErrorMessage(object):
    log = logging.getLogger(__name__)

    def __init__(
        self,
        exc_type=None,
        exc_value=None,
        exc_traceback=None,
        options=None,
        custom_message=None,
    ):
        self.className = exc_type.__name__ if exc_type is not None else None
        self.message = (
            custom_message or "%s: %s" % (exc_type.__name__, exc_value)
            if exc_type is not None
            else "RaygunSender.send_exception() called outside of except block"
        )
        self.stackTrace = []
        self.globalVariables = None

        try:
            frames = inspect.getinnerframes(exc_traceback)

            if frames:
                for frame in frames:
                    localVariables = None
                    if (
                        options is not None
                        and "transmitLocalVariables" in options
                        and options["transmitLocalVariables"] is True
                    ):
                        localVariables = self._get_locals(frame[0])

                    self.stackTrace.append(
                        {
                            "lineNumber": frame[2],
                            "className": frame[3],
                            "fileName": frame[1],
                            "methodName": frame[4][0] if frame[4] is not None else None,
                            "localVariables": localVariables,
                        }
                    )
                if (
                    options is not None
                    and "transmitGlobalVariables" in options
                    and options["transmitGlobalVariables"] is True
                    and len(frames) > 0
                ):
                    self.globalVariables = frames[-1][0].f_globals.copy()
        except Exception:
            pass
        finally:
            if "frames" in locals():
                del frames

        self.data = ""

        if isinstance(exc_value, Exception):
            nestedException = None

            if exc_value.__cause__:
                nestedException = exc_value.__cause__
            elif exc_value.__context__:
                nestedException = exc_value.__context__

            if nestedException is not None:
                self.innerError = RaygunErrorMessage(
                    type(nestedException),
                    nestedException,
                    nestedException.__traceback__,
                    options,
                )

        try:
            jsonpickle.encode(self, unpicklable=False)
        except Exception:
            if self.globalVariables:
                self.globalVariables = None

                try:
                    jsonpickle.encode(self, unpicklable=False)
                except Exception:
                    for frame in self.stackTrace:
                        if "localVariables" in frame:
                            frame["localVariables"] = None

    def check_and_modify_payload_size(self, options, max_size_kb=128):
        payload = jsonpickle.encode(self, unpicklable=False)

        while len(payload.encode("utf-8")) > max_size_kb * 1024:
            if not self._remove_largest_variable(
                options
            ):  # Failed to remove either local or global variable
                self.log.warning(
                    "Raygun4Py: Unable to reduce size of payload below 128kb, error will be discarded by Raygun ingestion API"
                )
                break

            payload = jsonpickle.encode(self, unpicklable=False)

    def _remove_largest_variable(self, options) -> bool:
        largest_global_var = None
        largest_global_size = 0

        largest_local_var = None
        largest_local_size = 0
        largest_local_frame = None

        # Find the largest global variable
        if self.globalVariables:
            for var, value in self.globalVariables.items():
                size = sys.getsizeof(value)
                if size > largest_global_size:
                    largest_global_size = size
                    largest_global_var = var

        # Find the largest local variable across all frames
        for frame in self.stackTrace:
            if "localVariables" in frame and frame["localVariables"]:
                for var, value in frame["localVariables"].items():
                    size = sys.getsizeof(value)
                    if size > largest_local_size:
                        largest_local_size = size
                        largest_local_var = var
                        largest_local_frame = frame

        if largest_global_size == 0 and largest_local_size == 0:
            return False

        # Decide which one to remove: the largest global or the largest local variable
        if largest_global_size >= largest_local_size and largest_global_var is not None:
            if (
                options is not None
                and "log_payload_size_limit_breaches" in options
                and options["log_payload_size_limit_breaches"] is True
            ):
                self.log.warning(
                    f"Raygun4Py: Removing global variable {largest_global_var} due to payload size limit"
                )

            self.globalVariables[largest_global_var] = "Removed"
        elif largest_local_var is not None and largest_local_frame is not None:
            if (
                options is not None
                and "log_payload_size_limit_breaches" in options
                and options["log_payload_size_limit_breaches"] is True
            ):
                self.log.warning(
                    f"Raygun4Py: Removing local variable {largest_local_var} due to payload size limit"
                )

            largest_local_frame["localVariables"][largest_local_var] = "Removed"

        return True

    def get_classname(self):
        return self.className

    def _get_locals(self, frame):
        result = {}
        localVars = getattr(frame, "f_locals", {})

        if "__traceback_hide__" not in localVars:
            for key in localVars:
                try:
                    # Note that str() *can* fail; thus protect against it as much as we can.
                    result[key] = str(localVars[key])
                except Exception as e:
                    try:
                        r = repr(localVars[key])
                    except Exception as re:
                        r = "Couldn't convert to repr due to {0}".format(re)
                    result[key] = (
                        "!!! Couldn't convert {0!r} (repr: {1}) due to {2!r} !!!".format(
                            key, r, e
                        )
                    )
        return result


class RaygunLoggerFallbackErrorMessage(object):

    def __init__(self, name, message, filename, funcName, lineno):
        self.className = "Logger (" + name + ")"
        self.message = message
        # Create a single stackTrace entry using logger data
        self.stackTrace = [
            {
                "lineNumber": lineno,
                "className": self.className,
                "fileName": filename,
                "methodName": funcName or "UnknownMethod",
                "localVariables": None,  # We don't have access to local variables
            }
        ]
        self.globalVariables = None  # We don't have access to global variables
        self.data = ""

        try:
            jsonpickle.encode(self, unpicklable=False)
        except Exception:
            for frame in self.stackTrace:
                if "localVariables" in frame:
                    frame["localVariables"] = None

    def get_classname(self):
        return self.className
