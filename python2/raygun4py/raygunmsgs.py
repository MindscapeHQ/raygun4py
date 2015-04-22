import traceback
import inspect

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

    def set_environment_details(self):
        self.raygunMessage.details['environment'] = {
            "processorCount": (
                multiprocessing.cpu_count() if USE_MULTIPROCESSING else "n/a"
            ),
            "architecture": platform.architecture()[0],
            "cpu": platform.processor(),
            "oSVersion": "%s %s" % (platform.system(), platform.release())
        }
        return self

    def set_exception_details(self, raygunExceptionMessage):
        self.raygunMessage.details['error'] = raygunExceptionMessage
        return self

    def set_client_details(self):
        self.raygunMessage.details['client'] = {
            "name": "raygun4py",
            "version": "2.2.0",
            "clientUrl": "https://github.com/MindscapeHQ/raygun4py"
        }
        return self

    def set_customdata(self, userCustomData):
        if type(userCustomData) is dict:
            self.raygunMessage.details['userCustomData'] = userCustomData
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
              "rawData": request['rawData'],
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

    def __init__(self, exc_type, exc_value, exc_traceback):
        self.className = exc_type.__name__
        self.message = "%s: %s" % (exc_type.__name__, exc_value)
        self.stackTrace = []

        try:
            frames = inspect.getinnerframes(exc_traceback)

            if frames:
                for frame in frames:
                    self.stackTrace.append({
                        'lineNumber': frame[2],
                        'className': frame[3],
                        'fileName': frame[1],
                        'methodName': frame[4][0],
                        'localVariables': self._get_locals(frame[0])
                    })
        finally:
            del frames

        self.data = ""

    def get_classname(self):
        return self.className

    def _get_locals(self, frame):
        result = {}
        localVars = getattr(frame, 'f_locals', {})

        if '__traceback_hide__' not in localVars:
            for key in localVars:
                result[key] = str(localVars[key])
            return result
