import sys, unittest, socket
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
        self.assertIsNotNone(self.builder.raygunMessage.details['machineName'])

    def test_customdata(self):
        self.builder.set_customdata({1: "one"})
        self.assertIsInstance(self.builder.raygunMessage.details['userCustomData'], dict)

    def test_tags(self):
        self.builder.set_tags([1, 2, 3])
        self.assertIsInstance(self.builder.raygunMessage.details['tags'], list)

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
    class GrandchildError(Exception):
        pass

    class ChildError(Exception):
        pass

    class ParentError(Exception):
        pass

    def setUp(self):
        try:
            self.parent()
        except Exception as e:
            self.theException = e
            self.exc_info = sys.exc_info()

    def parent(self):
            try:
                self.child()
            except TestRaygunErrorMessage.ChildError as exc:
                raise TestRaygunErrorMessage.ParentError("Parent message") from exc

    def child(self):
        try:
            raise TestRaygunErrorMessage.GrandchildError("GrandchildError")
        except Exception as ex:
            raise TestRaygunErrorMessage.ChildError("Child message")

    def test_exc_traceback_none_generates_empty_array(self):
        errorMessage = raygunmsgs.RaygunErrorMessage(int, 1, None, '')
        self.assertEqual(errorMessage.stackTrace, [])

    def test_parameter_classname(self):
        msg = raygunmsgs.RaygunErrorMessage(self.exc_info[0], self.exc_info[1], self.exc_info[2], type(self.theException))
        self.assertEqual(msg.className, TestRaygunErrorMessage.ParentError)

    def test_chained_exception_last_exception_caught_is_parent(self):
        self.assertIsInstance(self.theException.__context__, TestRaygunErrorMessage.ChildError)

    def test_chained_exception_cause_is_child(self):
        self.assertIsInstance(self.theException.__cause__, TestRaygunErrorMessage.ChildError)

    def test_chained_exception_childs_cause_is_grandchild(self):
        self.assertIsInstance(self.theException.__cause__.__context__, TestRaygunErrorMessage.GrandchildError)

def main():
    unittest.main()

if __name__ == '__main__':
    main()