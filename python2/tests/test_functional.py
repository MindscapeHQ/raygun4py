import unittest
import sys, logging, socket, os
from raygun4py import raygunprovider

class TestRaygun4PyFunctional(unittest.TestCase):

    def setUp(self):
        self.apiKey = "kImNMh/h98JZ233PUKv87g=="

    def test_sending(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise StandardError("Raygun4py manual sending test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            httpResult = client.send(exc_type, exc_value, exc_traceback)

            self.assertEquals(httpResult[0], 202)

    def test_sending_user(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_user({
            'firstName': 'foo',
            'fullName': 'foo bar',
            'email': 'foo@bar.com',
            'isAnonymous': False,
            'identifier': 'foo@bar.com'
          })

        try:
            raise Exception("Raygun4py manual sending test - user")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            httpResult = client.send(exc_type, exc_value, exc_traceback)

            self.assertEqual(httpResult[0], 202)

    def log_send(self, logger):
        try:
            raise StandardError("Raygun4py Logging Test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error("Logging with sending", exc_info = (exc_type, exc_value, exc_traceback))
            return 0

        return 1

    def log_nosend(self, logger):
        try:
            raise StandardError("Raygun4py Logging Test")
        except:
            logger.error("Logging without sending")
            return 0

        return 1

    def test_log_with_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEquals(0, self.log_send(logger))


    def test_log_without_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEquals(0, self.log_nosend(logger))