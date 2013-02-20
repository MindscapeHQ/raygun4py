import sys

class RaygunClient:

    apiKey = None

    def __init__(self, apiKey):
        if (apiKey):
            self.apiKey = apiKey
        else:
            print >> sys.stderr, "RaygunProvider error: ApiKey not set, errors will not be transmitted"

