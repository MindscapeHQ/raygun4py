import mock
import unittest2 as unittest

from webtest import TestApp
from webtest.debugapp import debug_app
from raygun4py.middleware.wsgi import Provider

class TestWSGIMiddleware(unittest.TestCase):

    def setUp(self):
        self.test_middleware = ExceptionMiddleware(debug_app)
        self.raygun_middleware = Provider(self.test_middleware, "XXXXXXXXXX")
        self.app = TestApp(app=self.raygun_middleware, lint=True)

        self.raygun_middleware.sender.send_exception = mock.MagicMock(return_value=True)

    def test_basic_exception(self):
        with self.assertRaises(Exception):
            self.app.get('/?error=t')

        self.raygun_middleware.sender.send_exception.assert_called_once()

    def test_json_post(self):
        self.test_middleware.raise_on_request = True

        with self.assertRaises(Exception):
            self.app.post_json('/foo/bar', params={
                'foo': 'bar'
            })

        self.raygun_middleware.sender.send_exception.assert_called_once()


class ExceptionMiddleware(object):

    def __init__(self, app):
        self.app = app
        self.raise_on_request = False

    def __call__(self, environ, start_response):
        appiter = None

        try:
            appiter = self.app(environ, start_response)

            if self.raise_on_request:
                raise Exception("test exception")

            for item in appiter:
                yield item
        except Exception:
            raise
        finally:
            if hasattr(appiter, 'close'):
                appiter.close()