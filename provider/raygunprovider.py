import sys, os, socket, logging
import jsonpickle, httplib
from provider import raygunmsgs

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

    def set_version(self, version):
        if isinstance(version, basestring):
            self.userversion = version    

    def send(self, exc_type, exc_value, exc_traceback, className = "Not provided", tags = None, userCustomData = None, httpRequest = None):
        rgExcept = raygunmsgs.RaygunErrorMessage(exc_type, exc_value, exc_traceback, className)
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
            .build()
            
    def _post(self, raygunMessage):
        json = jsonpickle.encode(raygunMessage, unpicklable=False)
        try:
            auth_header = 'Basic %s' % (":".join(["myusername","mypassword"]).encode('Base64').strip('\r\n'))
            headers = {"X-ApiKey": self.apiKey,
                       "Content-Type": "application/json",
                       "User-Agent": "raygun4py"}
            conn = httplib.HTTPSConnection(self.endpointhost, '443')
            conn.request('POST', self.endpointpath, json, headers)
            response = conn.getresponse()
        except Exception as e:
            print e
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