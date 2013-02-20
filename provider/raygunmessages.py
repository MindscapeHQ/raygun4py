from datetime import datetime

class RaygunMessage:

      def __init__(self):
            self.occurredOn = datetime.now()
            self.details = RaygunMessageDetails()


class RaygunMessageDetails:

    def __init__(self):
        self.machineName = None
