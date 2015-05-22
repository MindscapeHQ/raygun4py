import sys
import unittest2 as unittest
import socket
import inspect

from raygun4py import raygunmsgs

class TestRaygunMessageBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = raygunmsgs.RaygunMessageBuilder().new()
        self.request = {
            "headers": {
                "referer": "localhost",
                "user-Agent": "Mozilla"
            },
            "hostName": "localhost",
            "url": "/resource",
            "httpMethod": "GET",
            "ipAddress": "127.0.0.1",
            "queryString": None,
            "form": None,
            "rawData": None
        }

    def test_machinename(self):
        self.builder.set_machine_name(socket.gethostname())
        self.assertTrue(self.builder.raygunMessage.details['machineName'] != None)

    def test_customdata(self):
        self.builder.set_customdata({1: "one"})
        self.assertTrue(isinstance(self.builder.raygunMessage.details['userCustomData'], dict))

    def test_tags(self):
        self.builder.set_tags([1, 2, 3])
        self.assertTrue(isinstance(self.builder.raygunMessage.details['tags'], list))

    def test_request_ip(self):
        self.builder.set_request_details(self.request)
        self.assertEqual(self.builder.raygunMessage.details['request']['iPAddress'], '127.0.0.1')

    def test_user_fname(self):
        self.builder.set_user({
            'firstName': 'Foo',

        })
        self.assertEqual(self.builder.raygunMessage.details['user']['firstName'], 'Foo')

    def test_user_fullname(self):
        self.builder.set_user({
            'fullName': 'Foo Bar',
        })
        self.assertEqual(self.builder.raygunMessage.details['user']['fullName'], 'Foo Bar')

    def test_user_email(self):
        self.builder.set_user({
            'email': 'foo@bar.com',
        })
        self.assertEqual(self.builder.raygunMessage.details['user']['email'], 'foo@bar.com')

    def test_user_identifier(self):
        self.builder.set_user({
            'identifier': 'foo@bar.com',
        })
        self.assertEqual(self.builder.raygunMessage.details['user']['identifier'], 'foo@bar.com')

    def test_user_anon(self):
        self.builder.set_user({
            'isAnonymous': False
        })
        self.assertEqual(self.builder.raygunMessage.details['user']['isAnonymous'], False)

class TestRaygunErrorMessage(unittest.TestCase):
    class ParentError(Exception):
        pass

    def setUp(self):
        i_must_be_included = 'and i am'

        try:
            self.parent()
        except Exception as e:
            self.theException = e
            exc_info = sys.exc_info()
            self.msg = raygunmsgs.RaygunErrorMessage(exc_info[0], exc_info[1], exc_info[2], { 'transmitLocalVariables': True })

    def parent(self):
            raise TestRaygunErrorMessage.ParentError("Parent message")

    def test_exc_traceback_none_generates_empty_array(self):
        errorMessage = raygunmsgs.RaygunErrorMessage(int, 1, None, {})
        self.assertEqual(errorMessage.stackTrace, [])

    def test_classname(self):
        self.assertEqual(self.msg.className, 'ParentError')

    def test_local_variable(self):
        localVars = self.msg.__dict__['stackTrace'][0]['localVariables']

        self.assertTrue('i_must_be_included' in localVars)

    def test_methodname_none(self):
        originalGetinnerframes = inspect.getinnerframes
        inspect.getinnerframes = getinnerframes_mock_methodname_none

        errorMessage = raygunmsgs.RaygunErrorMessage(int, 1, None, { "transmitLocalVariables": False })

        self.assertEqual(errorMessage.__dict__['stackTrace'][0]['methodName'], None)

        inspect.getinnerframes = originalGetinnerframes

def getinnerframes_mock_methodname_none(exception):
    return [(
        'localVar',
        'fileName',
        'lineNumber',
        'className',
        None
    )]


def main():
    unittest.main()

if __name__ == '__main__':
    main()
