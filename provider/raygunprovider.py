import sys
from provider import raygunmessages

class RaygunSender:

    apiKey = None

    def __init__(self, apiKey):
        if (apiKey):
            self.apiKey = apiKey
        else:
            print >> sys.stderr, "RaygunProvider error: ApiKey not set, errors will not be transmitted"


    def send(self, exception):        
        self.post(self.createMessage(exception))


    def createMessage(self, exception):
        return RaygunMessageBuilder().build(exception)


    def post(self, raygunMessage):
        # print raygunMessage.occurredOn
        print "posting"


class RaygunMessageBuilder:

    raygunMessage = None

    def __init__(self):
        print "building"

    def build(self, exception):        
        return self
