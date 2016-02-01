import mock
import django
from django.conf import settings
from django.test.client import RequestFactory
from django.test import SimpleTestCase
from raygun4py.middleware.django import Provider

settings.configure(DEBUG=True, RAYGUN4PY_API_KEY='foo')
django.setup()


class DjangoProviderTests(SimpleTestCase):

    def setUp(self):
        request_factory = RequestFactory()
        self.get_request = request_factory.get('/foo')

    def test_map_request(self):
        provider = Provider()
        request_payload = provider._mapRequest(self.get_request)
        self.assertEqual(request_payload['url'], '/foo')
        self.assertEqual(request_payload['httpMethod'], 'GET')

    def test_get_django_environment(self):
        provider = Provider()
        environment_payload = provider._get_django_environment()
        self.assertEqual(environment_payload['frameworkVersion'], django.get_version())

    def test_process_exception_called(self):
        provider = Provider()
        provider.sender = mock.MagicMock(name='send_exception')

        try:
            raise Exception
        except Exception as e:
            provider.process_exception(self.get_request, e)

        self.assertEqual(len(provider.sender.mock_calls), 1)
