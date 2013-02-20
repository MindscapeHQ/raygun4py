import sys, os, socket
import jsonpickle, httplib
from provider import raygunmessages as rgmsgs

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


    def send(self, exception):        
        self.post(self.create_message(exception))


    def create_message(self, exception):
        return RaygunMessageBuilder().new() \
            .set_machine_name(socket.gethostname()) \
            .set_version() \
            .build()
            

    def post(self, raygunMessage):
        json = jsonpickle.encode(raygunMessage, unpicklable=False)
        try:
            auth_header = 'Basic %s' % (":".join(["myusername","mypassword"]).encode('Base64').strip('\r\n'))
            headers = {"X-ApiKey": self.apiKey,
                       "Content-Type": "application/json",
                       "User-Agent": "raygun4py"}
            # cert = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cert.pem")
            conn = httplib.HTTPSConnection('api.raygun.io', '443')
            conn.request("POST", "/entries", json, headers)
            response = conn.getresponse()
        except Exception as e:
            print e
        return response
                   

class RaygunMessageBuilder:

    def __init__(self):
        self.raygunMessage = rgmsgs.RaygunMessage()

    def new(self):
        return RaygunMessageBuilder()

    def build(self):
        return self.raygunMessage

    def set_machine_name(self, name):
        self.raygunMessage.details.machineName = name
        return self

    def set_environment_details(self):
        raise NotImplementedException()

    def set_exception_details(self, exception):
        raise NotImplementedException()

    def set_client_details(self):
        raise NotImplementedException()

    def set_user_custom_data(self):
        raise NotImplementedException()

    def set_http_details(self):
        raise NotImplementedException()

    def set_version(self):
        self.raygunMessage.details.version = "1.0"
        return self
