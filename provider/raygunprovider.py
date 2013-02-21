import sys, os, socket
import jsonpickle, httplib
from provider import raygunmsgs

class RaygunSender:

    apiKey = None

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

    def send(self, exc_type, exc_value, exc_traceback, className = "Not provided"):
        rgExcept = raygunmsgs.RaygunErrorMessage(exc_type, exc_value, exc_traceback, className)
        return self.post(self.create_message(rgExcept))

    def create_message(self, raygunExceptionMessage):
        return raygunmsgs.RaygunMessageBuilder().new() \
            .set_machine_name(socket.gethostname()) \
            .set_version(self.userversion) \
            .set_client_details() \
            .set_exception_details(raygunExceptionMessage) \
            .build()
            
    def post(self, raygunMessage):
        json = jsonpickle.encode(raygunMessage, unpicklable=False)
        try:
            auth_header = 'Basic %s' % (":".join(["myusername","mypassword"]).encode('Base64').strip('\r\n'))
            headers = {"X-ApiKey": self.apiKey,
                       "Content-Type": "application/json",
                       "User-Agent": "raygun4py"}
            conn = httplib.HTTPSConnection('api.raygun.io', '443')
            conn.request("POST", "/entries", json, headers)
            response = conn.getresponse()
        except Exception as e:
            print e
        return response.status, response.reason
