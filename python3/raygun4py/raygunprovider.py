import sys, os, socket, logging
import jsonpickle, http.client
from raygun4py import raygunmsgs

class RaygunSender:

    apiKey = None
    endpointhost = 'api.raygun.io'
    endpointpath = '/entries'

    def __init__(self, apiKey):
        if (apiKey):
            self.apiKey = apiKey
        else:
            print("RaygunProvider error: ApiKey not set, errors will not be transmitted", end="\n", file=sys.stderr)

        try:
            import ssl
        except ImportError:
            print(("RaygunProvider error: No SSL support available, cannot send. Please"
                                  "compile the socket module with SSL support."), end="\n", file=sys.stderr)

        self.userversion = "Not defined"
        self.user = None

    def set_version(self, version):
        if isinstance(version, str):
            self.userversion = version

    def set_user(self, user):
        self.user = user;

    def send(self, exc_type, exc_value, exc_traceback, className = "Not provided", tags = None, userCustomData = None, httpRequest = None):
        rgExcept = raygunmsgs.RaygunErrorMessage(exc_type, exc_value, exc_traceback)

        return self._post(self._create_message(rgExcept, tags, userCustomData, httpRequest))

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

    def _post(self, raygunMessage):
        payload = jsonpickle.encode(raygunMessage, unpicklable=False)

        try:
            headers = {
              "X-ApiKey": self.apiKey,
              "Content-Type": "application/json",
              "User-Agent": "raygun4py"
            }

            conn = http.client.HTTPSConnection(self.endpointhost, '443')
            conn.request('POST', self.endpointpath, payload, headers)
            response = conn.getresponse()
        except Exception as e:
            raise(e)
            return 400, "Exception: Could not send"

        return response.status, response.reason

class RaygunHandler(logging.Handler):
    def __init__(self, apiKey, version = None):
        logging.Handler.__init__(self)
        self.sender = RaygunSender(apiKey)
        self.version = version

    def emit(self, record):
        if record.exc_info:
            exc = record.exc_info

            tags = None
            userCustomData = { "Logger Message" : record.msg }
            request = None
            className = None
            self.sender.send(exc[0], exc[1], exc[2], className, tags, userCustomData, request)