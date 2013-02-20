import sys
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

    def set_exception_details(self, exception):
        self.raygunMessage.details.error = RaygunErrorMessage(exception)
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

      def __init__(self, exception):
            print sys.exc_info()
            self.message = exception.message
            self.stacktrace = [RaygunErrorStackTraceLineMessage(0, "myclass", "myfile", "mymethod")]
            self.classname = "fuh"
            self.data = "wah"

class RaygunErrorStackTraceLineMessage:
      
      def __init__(self, lineName, className, fileName, methodName):
            self.linenumber = lineName
            self.classname = className
            self.filename = fileName
            self.methodname = methodName

class RaygunRequestMessage:
      pass
