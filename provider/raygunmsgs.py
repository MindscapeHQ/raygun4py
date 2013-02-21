import sys, traceback
from datetime import datetime

class RaygunMessageBuilder:

    def __init__(self):
        self.raygunMessage = RaygunMessage()

    def new(self):
        return RaygunMessageBuilder()

    def build(self):
        return self.raygunMessage

    def set_machine_name(self, name):
        self.raygunMessage.details.machineName = name
        return self

    def set_environment_details(self):
        raise NotImplementedException()

    def set_exception_details(self, raygunExceptionMessage):
        self.raygunMessage.details.error = raygunExceptionMessage
        return self

    def set_client_details(self):
        self.raygunMessage.details.client = RaygunClientMessage()
        return self

    def set_user_custom_data(self):
        self.raygunMessage

    def set_http_details(self):
        self.raygunMessage.details.request = RaygunRequestMessage()

    def set_version(self, version):
        self.raygunMessage.details.version = version
        return self

class RaygunMessage:

      def __init__(self):
            self.occurredOn = datetime.utcnow() 
            self.details = RaygunMessageDetails()

class RaygunMessageDetails:
      pass

class RaygunClientMessage:

      def __init__(self):
            self.name = "raygun4py"
            self.version = "0.1"
            self.clienturl = "https://github.com/MindscapeHQ/raygun4py"

class RaygunErrorMessage:

      def __init__(self, exc_type, exc_value, exc_traceback, className):
            self.message = "%s: %s" % (exc_type.__name__, exc_value)
            self.stacktrace = []
            for trace in traceback.extract_tb(exc_traceback):
                  self.stacktrace.append(RaygunErrorStackTraceLineMessage(trace))

            self.classname = className
            self.data = "wah"

class RaygunErrorStackTraceLineMessage:
      
      def __init__(self, trace):
            self.linenumber = trace[1]
            self.classname = ""
            self.filename = trace[0]
            self.methodname = trace[2]

class RaygunRequestMessage:
      pass
