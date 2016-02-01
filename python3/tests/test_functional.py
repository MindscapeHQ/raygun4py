# coding=utf-8

import unittest
import sys, logging, socket, os
from raygun4py import raygunprovider

class TestRaygun4PyFunctional(unittest.TestCase):

    def setUp(self):
        self.apiKey = "kImNMh/h98JZ233PUKv87g=="

    def test_python3_new_sending(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py3 Python3 send")
        except Exception as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult[0], 202)

    def test_sending_exc_info(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py3 manual sending test")
        except:
            exc_info = sys.exc_info()
            httpResult = client.send_exception(exc_info=exc_info)

            self.assertEqual(httpResult[0], 202)

    def test_sending_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py3 manual sending test")
        except Exception as e:
            httpResult = client.send_exception(exception=e)

            self.assertEqual(httpResult[0], 202)

    def test_sending_auto(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py3 exception (auto)")
        except Exception as e:
            httpResult = client.send_exception()

            self.assertEqual(httpResult[0], 202)

    def test_sending_chained_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            try:
                raise Exception("Nested child test_python3_new_sending")
            except:
                raise Exception("Nested parent py3")
        except:
            exc_info = sys.exc_info()
            httpResult = client.send_exception(exc_info=exc_info)

            self.assertEqual(httpResult[0], 202)

    def test_send_with_version(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_version('v1.0.0')

        try:
            raise Exception("Raygun4py3 manual sending test - version")
        except:
            httpResult = client.send_exception(exc_info=sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def test_send_with_tags(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py manual sending test - tags")
        except:
            httpResult = client.send_exception(exc_info=sys.exc_info(), tags=["I am a tag"])

            self.assertEqual(httpResult[0], 202)

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
            raise Exception("Raygun4py3 manual sending test - user")
        except:
            exc_info = sys.exc_info()
            httpResult = client.send_exception(exc_info=exc_info)

            self.assertEqual(httpResult[0], 202)

    def log_send(self, logger):
        try:
            raise Exception("Raygun4py3 Logging Test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error("Logging with sending", exc_info=sys.exc_info())
            return 0

        return 1

    def log_nosend(self, logger):
        try:
            raise Exception("Raygun4py3 Logging Test")
        except:
            logger.error("Logging without sending")
            return 0

        return 1

    def test_log_with_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEqual(0, self.log_send(logger))


    def test_log_without_sending(self):
        logger = logging.getLogger("mylogger")
        rgHandler = raygunprovider.RaygunHandler(self.apiKey)
        logger.addHandler(rgHandler)

        self.assertEqual(0, self.log_nosend(logger))

    def test_localvariables(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            foo = 'bar'
            raise Exception("Raygun4py3 functional test - local variables")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_localvariables_multilevels(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            scope = 'parent'
            child()
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_before_send_callback(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.on_before_send(before_send_mutate_payload)

        try:
            raise Exception("Raygun4py3 functional test - on_before_send")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())
        
        self.assertEqual(httpResult[0], 202)

    def test_before_send_callback_sets_none_cancels_send(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.on_before_send(before_send_cancel_send)

        try:
            raise Exception("Raygun4py3 functional test - on_before_send")
        except Exception as e:
            result = client.send_exception(e, exc_info = sys.exc_info())
        
        self.assertIsNone(result)

    def test_request(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - on_before_send")
        except Exception as e:
            result = client.send_exception(request={})

            self.assertEqual(result[0], 202)

    def test_http_request(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - on_before_send")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_utf8_message(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("ΔΔΔΔ")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_utf8_localvariable(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        the_variable = 'ᵫ'

        try:
            raise Exception("Raygun4py3: utf8 local variable")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_bytestring_localvariable(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        byte_string = b'\x8d\x80\x92uK!M\xed'

        try:
            raise Exception("Raygun4py3: bytestring local variable")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_localvariables_unicode(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            sigma = u'\u2211'
            raise Exception("Raygun4py3 functional test - local variable - unicode")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_localvariables_cause_str_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        class StrFailingClass(object):
            def __str__(self):
                raise Exception("I failed to stringify myself")

        instance = StrFailingClass()

        try:
            raise Exception("Raygun4py3 functional test - local variable - cause an str exception")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            
def before_send_mutate_payload(message):
    message['newKey'] = 'newValue'
    return message

def before_send_cancel_send(message):
    return None

def child():
    throwerScope = 'child'
    raise Exception("Raygun4py3 functional test - local variables multi levels")