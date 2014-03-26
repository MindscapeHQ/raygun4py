import unittest, socket
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

    def test_user(self):
        self.builder.set_user('user1')
        self.assertEqual(self.builder.raygunMessage.details['user'], { 'identifier': 'user1' })


def main():
    unittest.main()

if __name__ == '__main__':
    main()