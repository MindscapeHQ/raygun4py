# coding=utf-8

import unittest2 as unittest
import sys, logging, socket, os
from raygun4py import raygunprovider

class TestRaygun4PyFunctional(unittest.TestCase):

    def setUp(self):
        self.apiKey = "kImNMh/h98JZ233PUKv87g=="

    def test_send_with_user(self):
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
            httpResult = client.send_exception(exc_info=sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def test_send_with_version(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_version('v1.0.0')

        try:
            raise Exception("Raygun4py manual sending test - version")
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

    def test_send_exception_no_args(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception")
        except:
            httpResult = client.send_exception()

            self.assertEqual(httpResult[0], 202)

    def test_send_exception_with_exc_info(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise StandardError("Raygun4py manual sending test")
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            httpResult = client.send_exception(exc_info = sys.exc_info())


    def test_send_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception")
        except Exception as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult[0], 202)

    def test_send_exception_with_exc_info(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise Exception("Raygun4py functional test - Py2 send_exception with exc_info")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())

            self.assertEqual(httpResult[0], 202)

    def test_send_exception_subclass(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            raise CustomException("Raygun4py functional test - Py2 send_exception with custom exception")
        except CustomException as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult[0], 202)

    def test_ignore_exception(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.ignore_exceptions(['CustomException'])

        try:
            raise CustomException("This test should not send an exception")
        except CustomException as e:
            httpResult = client.send_exception(e)

            self.assertEqual(httpResult, None)

    def test_filter_keys_202(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.filter_keys(['environment'])

        try:
            raise Exception("Raygun4py functional test - Py2 filter_keys")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())

        self.assertEqual(httpResult[0], 202)

    @unittest.skip('Requires a proxy, skipping for Travis')
    def test_proxy(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.set_proxy('127.0.0.1', 3128)

        try:
            raise Exception("Raygun4py functional test - Py2 set_proxy")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())

        self.assertEqual(httpResult[0], 202)


    def test_before_send_callback(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.on_before_send(before_send_mutate_payload)

        try:
            raise Exception("Raygun4py functional test - on_before_send")
        except Exception as e:
            httpResult = client.send_exception(e, exc_info = sys.exc_info())

        self.assertEqual(httpResult[0], 202)

    def test_before_send_callback_sets_none_cancels_send(self):
        client = raygunprovider.RaygunSender(self.apiKey)
        client.on_before_send(before_send_cancel_send)

        try:
            raise Exception("Raygun4py functional test - on_before_send")
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

    def test_localvariables(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            foo = 'bar'
            raise Exception("Raygun4py functional test - local variables")
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
            raise Exception("Raygun4py2: utf8 local variable")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_bytestring_localvariable(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        byte_string = b'\x8d\x80\x92uK!M\xed'

        try:
            raise Exception("Raygun4py2: bytestring local variable")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

    def test_localvariables_unicode(self):
        client = raygunprovider.RaygunSender(self.apiKey)

        try:
            sigma = u'\u2211'
            raise Exception("Raygun4py functional test - local variable - unicode")
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
            raise Exception("Raygun4py functional test - local variable - cause an str exception")
        except Exception as e:
            result = client.send_exception(httpRequest={})

            self.assertEqual(result[0], 202)

class CustomException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def before_send_mutate_payload(message):
    message['newKey'] = 'newValue'
    return message

def before_send_cancel_send(message):
    return None

def child():
    throwerScope = 'child'
    raise Exception("Raygun4py functional test - local variables multi levels")