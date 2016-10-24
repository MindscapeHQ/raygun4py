import sys
import os
import inspect
import jsonpickle

try:
    import multiprocessing
    USE_MULTIPROCESSING = True
except ImportError:
    USE_MULTIPROCESSING = False

import platform
from datetime import datetime


class RaygunMessageBuilder:

    def __init__(self):
        self.raygunMessage = RaygunMessage()

    def new(self):
        return RaygunMessageBuilder()

    def build(self):
        return self.raygunMessage

    def set_machine_name(self, name):
        self.raygunMessage.details['machineName'] = name
        return self

    def set_environment_details(self, extra_environment_data):
        self.raygunMessage.details['environment'] = {
            "environmentVariables": dict(os.environ.data) if hasattr(os.environ, 'data') else None,
            "runtimeLocation": sys.executable,
            "runtimeVersion": 'Python ' + sys.version
        }

        # Wrap these so we gracefully fail if we cannot access the system details for any reason
        try:
            self.raygunMessage.details['environment']["processorCount"] = (
                multiprocessing.cpu_count() if USE_MULTIPROCESSING else "n/a"
            )
        except Exception: # pragma: no cover
            pass

        try:
            self.raygunMessage.details['environment']["architecture"] = platform.architecture()[0]
        except Exception: # pragma: no cover
            pass

        try:
            self.raygunMessage.details['environment']["cpu"] = platform.processor()
        except Exception: # pragma: no cover
            pass

        try:
            self.raygunMessage.details['environment']["oSVersion"] = "%s %s" % \
                (platform.system(), platform.release())
        except Exception: # pragma: no cover
            pass

        if extra_environment_data is not None:
            merged = extra_environment_data.copy()
            merged.update(self.raygunMessage.details['environment'])
            self.raygunMessage.details['environment'] = merged

        return self

    def set_exception_details(self, raygunExceptionMessage):
        self.raygunMessage.details['error'] = raygunExceptionMessage
        return self

    def set_client_details(self):
        self.raygunMessage.details['client'] = {
            "name": "raygun4py",
            "version": "3.1.3",
            "clientUrl": "https://github.com/MindscapeHQ/raygun4py"
        }
        return self

    def set_customdata(self, user_custom_data):
        if type(user_custom_data) is dict:
            self.raygunMessage.details['userCustomData'] = user_custom_data
        return self

    def set_tags(self, tags):
        if type(tags) is list or tuple:
            self.raygunMessage.details['tags'] = tags
        return self

    def set_request_details(self, request):
        if request:
            self.raygunMessage.details['request'] = {
                "hostName": request['hostName'],
                "url": request['url'],
                "httpMethod": request['httpMethod'],
                "queryString": request['queryString'],
                "form": request['form'],
                "headers": request['headers'],
                "rawData": request['rawData']
            }

            if 'ipAddress' in request:
                self.raygunMessage.details['request']['iPAddress'] = request['ipAddress']
            elif 'iPAddress' in request:
                self.raygunMessage.details['request']['iPAddress'] = request['iPAddress']

        return self

    def set_version(self, version):
        self.raygunMessage.details['version'] = version
        return self

    def set_user(self, user):
        if user is not None:
            self.raygunMessage.details['user'] = user
        return self


class RaygunMessage:

    def __init__(self):
        self.occurredOn = datetime.utcnow()
        self.details = {}

    def get_error(self):
        return self.details['error']

    def get_details(self):
        return self.details


class RaygunErrorMessage:

    def __init__(self, exc_type, exc_value, exc_traceback, options):
        self.className = exc_type.__name__
        self.message = "%s: %s" % (exc_type.__name__, exc_value)
        self.stackTrace = []

        frames = None
        try:
            frames = inspect.getinnerframes(exc_traceback)

            if frames:
                for frame in frames:
                    localVariables = None
                    if 'transmitLocalVariables' in options and options['transmitLocalVariables'] is True:
                        localVariables = self._get_locals(frame[0])

                    self.stackTrace.append({
                        'lineNumber': frame[2],
                        'className': frame[3],
                        'fileName': frame[1],
                        'methodName': frame[4][0] if frame[4] is not None else None,
                        'localVariables': localVariables
                    })
                if 'transmitGlobalVariables' in options and options['transmitGlobalVariables'] is True and len(frames) > 0:
                    self.globalVariables = frames[-1][0].f_globals
        finally:
            del frames

        self.data = ""

        try:
            jsonpickle.encode(self, unpicklable=False)
        except Exception as e:
            if self.globalVariables:
                self.globalVariables = None

                try:
                    jsonpickle.encode(self, unpicklable=False)
                except Exception as e:
                    for frame in self.stackTrace:
                        if 'localVariables' in frame:
                            frame.localVariables = None

    def get_classname(self):
        return self.className

    def _get_locals(self, frame):
        result = {}
        localVars = getattr(frame, 'f_locals', {})

        if '__traceback_hide__' not in localVars:
            for key in localVars:
                try:
                    # Note that str() *can* fail; thus protect against it as much as we can.
                    if type(localVars[key]) is unicode:
                        result[key] = localVars[key]
                    else:
                        result[key] = str(localVars[key])
                except Exception as e:
                    try:
                        r = repr(localVars[key])
                    except Exception as re:
                        r = "Couldn't convert to repr due to {0}".format(re)
                    result[key] = "!!! Couldn't convert {0!r} (repr: {1}) due to {2!r} !!!".format(key, r, e)
            return result