import sys, unittest, socket
import inspect
import jsonpickle
from raygun4py import raygunmsgs, raygunprovider


class TestRaygunMessageBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = raygunmsgs.RaygunMessageBuilder({}).new()
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

        # https://www.python.org/dev/peps/pep-3333/#environ-variables
        self.raw_wsgi_request = {
            "HTTP_PRAGMA": "no-cache",
            "HTTP_COOKIE": "test-cookie=foo",
            "SCRIPT_NAME": "",
            "REQUEST_METHOD": "GET",
            "HTTP_HOST": "localhost:1234",
            "PATH_INFO": "/resource-wsgi",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "QUERY_STRING": "query=testme",
            "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
            "HTTP_CACHE_CONTROL": "no-cache",
            "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "HTTP_USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "HTTP_REFERER": "https://www.google.com/",
            "HTTP_CONNECTION": "keep-alive",
            "SERVER_NAME": "localhost",
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.9",
            "wsgi.url_scheme": "http",
            "SERVER_PORT": "1234",
            "HTTP_ACCEPT_ENCODING": "gzip, deflate, br"
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

    def test_request_ip_from_remote_addr(self):
        self.builder.set_request_details(self.raw_wsgi_request)
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

    def test_wsgi_fallbacks(self):
        self.builder.set_request_details(self.raw_wsgi_request)
        self.assertEqual(self.builder.raygunMessage.details['request']['hostName'], 'localhost:1234')
        self.assertEqual(self.builder.raygunMessage.details['request']['url'], '/resource-wsgi')
        self.assertEqual(self.builder.raygunMessage.details['request']['httpMethod'], 'GET')
        self.assertEqual(self.builder.raygunMessage.details['request']['queryString'], 'query=testme')

    def test_wsgi_standard_header_names(self):
        self.builder.set_request_details(self.raw_wsgi_request)
        self.assertEqual(self.builder.raygunMessage.details['request']['headers']['User-Agent'],
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
        self.assertEqual(self.builder.raygunMessage.details['request']['headers']['Referer'],
                        "https://www.google.com/")

    def test_set_request_details_allows_chaining(self):
        self.builder \
                .set_request_details(self.raw_wsgi_request) \
                .set_tags(['foo', 'bar'])

    def test_environment_variables(self):
        self.builder.set_environment_details(None)

        self.assertIsNotNone(self.builder.raygunMessage.details['environment']['environmentVariables'])

    def test_environment_variables_are_ignored(self):
        self.builder.options = {
            'transmit_environment_variables': False
        }
        self.builder.set_environment_details(None)

        self.assertIsNone(self.builder.raygunMessage.details['environment']['environmentVariables'])


class TestRaygunErrorMessage(unittest.TestCase):
    ONEHUNDRED_AND_FIFTEY_KB = 150 * 1024

    def create_string_of_size(self, size_in_bytes):
        return "a" * size_in_bytes
    
    def get_string_size(self, s):
        return len(s)
    
    def find_local_variable(self, stack_trace, variable_name):
        for frame in stack_trace:
            if 'localVariables' in frame and frame['localVariables']:
                if variable_name in frame['localVariables']:
                    return frame['localVariables'][variable_name]
                
        return None

    def setUp(self):
        self.client = raygunprovider.RaygunSender("Dummy API key")

    def test_global_reference_kept(self):
        global globalReference 
        globalReference = self.create_string_of_size(self.ONEHUNDRED_AND_FIFTEY_KB)

        try:
            raise Exception()
        except Exception as e:
            self.client.send_exception()

        self.assertEqual(self.get_string_size(globalReference), self.ONEHUNDRED_AND_FIFTEY_KB)

        del globalReference

    def test_remove_global_too_large(self):
        global globalReference
        globalReference = self.create_string_of_size(self.ONEHUNDRED_AND_FIFTEY_KB)

        try:
            raise Exception()
        except Exception as e:
            exc_info = sys.exc_info()

            msg = raygunmsgs.RaygunErrorMessage(exc_info[0], exc_info[1], exc_info[2], { 'transmitGlobalVariables': True })

            msg_clone = jsonpickle.loads(jsonpickle.dumps(msg))
            msg_clone.check_and_modify_payload_size({'enforce_payload_size_limit' : True})

            self.assertEqual(msg_clone.globalVariables['globalReference'], "Removed")

        del globalReference

    def test_remove_local_too_large(self):
        localReference = self.create_string_of_size(self.ONEHUNDRED_AND_FIFTEY_KB)

        try:
            raise Exception()
        except Exception as e:
            exc_info = sys.exc_info()

            msg = raygunmsgs.RaygunErrorMessage(exc_info[0], exc_info[1], exc_info[2], { 'transmitLocalVariables' : True })

            msg_clone = jsonpickle.loads(jsonpickle.dumps(msg))
            msg_clone.check_and_modify_payload_size({'enforce_payload_size_limit' : True})

            self.assertEqual(self.find_local_variable(msg.stackTrace, "localReference"), "Removed")

    def test_remove_larger_varaible(self):
        global globalReference

        globalReference = self.create_string_of_size(80 * 1024)
        localReference = self.create_string_of_size(64 * 1024)

        try:
            raise Exception()
        except Exception as e:
            exc_info = sys.exc_info()

            msg = raygunmsgs.RaygunErrorMessage(exc_info[0], exc_info[1], exc_info[2], { 'transmitGlobalVariables': True, 'transmitLocalVariables' : True })

            msg_clone = jsonpickle.loads(jsonpickle.dumps(msg))
            msg_clone.check_and_modify_payload_size({'enforce_payload_size_limit' : True})

            self.assertEqual(msg_clone.globalVariables['globalReference'], "Removed")
            self.assertEqual(self.find_local_variable(msg.stackTrace, "localReference"), localReference)
        
        del globalReference

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

            exc_info = sys.exc_info()
            self.msg = raygunmsgs.RaygunErrorMessage(exc_info[0], exc_info[1], exc_info[2], { 'transmitLocalVariables': True })

    def parent(self):
            try:
                self.child()
            except TestRaygunErrorMessage.ChildError as exc:
                raise TestRaygunErrorMessage.ParentError("Parent message") from exc

    def child(self):
        try:
            raise TestRaygunErrorMessage.GrandchildError("Grandchild message")
        except Exception as ex:
            raise TestRaygunErrorMessage.ChildError("Child message")

    def test_exc_traceback_none_generates_empty_array(self):
        error_message = raygunmsgs.RaygunErrorMessage(Exception, None, None, {})
        self.assertEqual(error_message.stackTrace, [])

    def test_classname(self):
        self.assertEqual(self.msg.className, 'ParentError')

    def test_chained_exception_message_parent_has_nested_child(self):
        self.assertEqual(self.msg.innerError.className, 'ChildError')
        pass

    def test_chained_exception_message_child_has_nested_grandchild(self):
        self.assertEqual(self.msg.innerError.innerError.className, 'GrandchildError')
        pass

    def test_chained_exception_nested_child_message(self):
        self.assertEqual(self.msg.innerError.message, 'ChildError: Child message')
        pass

    def test_chained_exception_nested_grandchild_message(self):
        self.assertEqual(self.msg.innerError.innerError.message, 'GrandchildError: Grandchild message')
        pass

    def test_chained_exception_last_exception_caught_is_parent(self):
        self.assertIsInstance(self.theException.__context__, TestRaygunErrorMessage.ChildError)

    def test_chained_exception_cause_is_child(self):
        self.assertIsInstance(self.theException.__cause__, TestRaygunErrorMessage.ChildError)

    def test_chained_exception_childs_cause_is_grandchild(self):
        self.assertIsInstance(self.theException.__cause__.__context__, TestRaygunErrorMessage.GrandchildError)

    def test_methodname_none(self):
        original_getinnerframes = inspect.getinnerframes
        inspect.getinnerframes = getinnerframes_mock_methodname_none

        error_message = raygunmsgs.RaygunErrorMessage(int, 1, None, { "transmitLocalVariables": False })

        self.assertEqual(error_message.__dict__['stackTrace'][0]['methodName'], None)

        inspect.getinnerframes = original_getinnerframes

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
