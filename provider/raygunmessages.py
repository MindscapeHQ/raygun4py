from datetime import datetime

class RaygunMessage:

      occurredOn = None
      details = None

      def __init__(self):
            occurredOn = datetime.now()
