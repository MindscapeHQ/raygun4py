import sys
import traceback
import multiprocessing
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
        self.raygunMessage.details.machineName = name
        return self

    def set_environment_details(self):
        self.raygunMessage.details.environment = RaygunEnvironmentMessage()
        return self

    def set_exception_details(self, raygunExceptionMessage):
        self.raygunMessage.details.error = raygunExceptionMessage
        return self

    def set_client_details(self):
        self.raygunMessage.details.client = RaygunClientMessage()
        return self

    def set_customdata(self, userCustomData):
          if type(userCustomData) is dict:
                self.raygunMessage.details.userCustomData = userCustomData
          return self

    def set_tags(self, tags):
          if type(tags) is list or tuple:
                self.raygunMessage.details.tags = tags
          return self

    def set_request_details(self, request):
        if request:
          self.raygunMessage.details.request = RaygunRequestMessage(request)                  
        return self

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
            self.clientUrl = "https://github.com/MindscapeHQ/raygun4py"

class RaygunErrorMessage:

      def __init__(self, exc_type, exc_value, exc_traceback, className):
            self.message = "%s: %s" % (exc_type.__name__, exc_value)
            self.stackTrace = []
            for trace in traceback.extract_tb(exc_traceback):         
                  self.stackTrace.append(RaygunErrorStackTraceLineMessage(trace))            
            self.className = trace[2]
            self.data = ""

class RaygunErrorStackTraceLineMessage:
      
      def __init__(self, trace):
            self.lineNumber = trace[1]
            self.className = trace[2]
            self.fileName = trace[0]
            self.methodName = trace[3]            
            print "Class ", trace[2]
            print "Method ", trace[3]

class RaygunRequestMessage:
      
      def __init__(self, request):            
            self.hostName = request['hostName']
            self.url = request['url']
            self.httpMethod = request['httpMethod']
            self.ipAddress = request['ipAddress']
            self.queryString = request['queryString']
            self.form = request['form']
            self.headers = request['headers']
            self.rawData = request['rawData']

class RaygunEnvironmentMessage:

      def __init__(self):
            self.processorCount = multiprocessing.cpu_count()
            self.architecture = platform.architecture()[0]
            self.cpu = platform.processor()
            self.osVersion = "%s %s" % (platform.system(), platform.release())
