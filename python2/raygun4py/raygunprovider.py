import sys
import os
import socket
import logging
import jsonpickle
import httplib
from raygun4py import raygunmsgs
from raygun4py import utilities


class RaygunSender:

    apiKey = None
    endpointhost = 'api.raygun.io'
    endpointpath = '/entries'

    def __init__(self, apiKey):
        if (apiKey):
            self.apiKey = apiKey
        else:
            print >> sys.stderr, "RaygunProvider error: ApiKey not set, errors will not be transmitted"

        try:
            import ssl
        except ImportError:
            print >> sys.stderr, ("RaygunProvider error: No SSL support available, cannot send. Please"
                                  "compile the socket module with SSL support.")
        self.userversion = "Not defined"
        self.user = None
        self.ignoredExceptions = []
        self.filteredKeys = []

    def set_version(self, version):
        if isinstance(version, basestring):
            self.userversion = version

    def set_user(self, user):
        self.user = user

    def ignore_exceptions(self, exceptions):
        if isinstance(exceptions, list):
            self.ignoredExceptions = exceptions

    def filter_keys(self, keys):
        if isinstance(keys, list):
            self.filteredKeys = keys

    def use_proxy(self, proxy):
        pass

    def track_exception(self, exc_info=None, **kwargs):
        if exc_info is None:
            exc_info = sys.exc_info()

        exc_type, exc_value, exc_traceback = exc_info

        errorMessage = raygunmsgs.RaygunErrorMessage(exc_type, exc_value, exc_traceback)

        try:
            del exc_type, exc_value, exc_traceback
        except Exception as e:
            raise

        tags, customData, httpRequest = self._parse_args(kwargs)
        message = self._create_message(errorMessage, tags, customData, httpRequest)
        message = self._transform_message(message)

        return self._post(message)

    def send_exception(self, exception, exc_info=None, **kwargs):
        if exc_info is None:
            exc_info = sys.exc_info()

        exc_type, exc_value, exc_traceback = exc_info

        errorMessage = raygunmsgs.RaygunErrorMessage(type(exception), exception, exc_traceback)

        try:
            del exc_type, exc_value, exc_traceback
        except Exception as e:
            raise

        tags, customData, httpRequest = self._parse_args(kwargs)
        message = self._create_message(errorMessage, tags, customData, httpRequest)
        message = self._transform_message(message)

        if message is not None:
            return self._post(message)

    def _parse_args(errorMessage, kwargs):
        tags = kwargs['tags'] if 'tags' in kwargs else None
        customData = kwargs['userCustomData'] if 'userCustomData' in kwargs else None
        httpRequest = kwargs['httpRequest'] if 'httpRequest' in kwargs else None

        return tags, customData, httpRequest

    def _create_message(self, raygunExceptionMessage, tags, userCustomData, httpRequest):
        return raygunmsgs.RaygunMessageBuilder().new() \
            .set_machine_name(socket.gethostname()) \
            .set_version(self.userversion) \
            .set_client_details() \
            .set_exception_details(raygunExceptionMessage) \
            .set_environment_details() \
            .set_tags(tags) \
            .set_customdata(userCustomData) \
            .set_request_details(httpRequest) \
            .set_user(self.user) \
            .build()

    def _transform_message(self, message):
        message = utilities.ignore_exceptions(self.ignoredExceptions, message)

        if message is not None:
            message = utilities.filter_keys(self.filteredKeys, message)

        return message

    def _post(self, raygunMessage):
        json = jsonpickle.encode(raygunMessage, unpicklable=False)

        try:
            auth_header = 'Basic %s' % (":".join(["myusername", "mypassword"]).encode('Base64').strip('\r\n'))
            headers = {
                "X-ApiKey": self.apiKey,
                "Content-Type": "application/json",
                "User-Agent": "raygun4py"
            }

            conn = httplib.HTTPSConnection(self.endpointhost, '443')
            conn.request('POST', self.endpointpath, json, headers)
            response = conn.getresponse()
        except Exception as e:
            print e
            return 400, "Exception: Could not send"
        return response.status, response.reason


class RaygunHandler(logging.Handler):
    def __init__(self, apiKey, version=None):
        logging.Handler.__init__(self)
        self.sender = RaygunSender(apiKey)
        self.version = version

    def emit(self, record):
        if record.exc_info:
            exc = record.exc_info

            userCustomData = {
                "Logger Message": record.msg
            }
            self.sender.track_exception(exc, userCustomData=userCustomData)
