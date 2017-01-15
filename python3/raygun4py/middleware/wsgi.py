import logging
from raygun4py import raygunprovider

log = logging.getLogger(__name__)


class Provider(object):

    def __init__(self, app, apiKey):
        self.app = app
        self.sender = raygunprovider.RaygunSender(apiKey)

    def __call__(self, environ, start_response):
        if not self.sender:
            log.error("Raygun-WSGI: Cannot send as provider not attached")

        iterable = None

        try:
            iterable = self.app(environ, start_response)
            for event in iterable:
                yield event

        except Exception as e:
            request = self.build_request(environ)
            self.sender.send_exception(exception=e, request=request)
            raise

        finally:
            if hasattr(iterable, 'close'):
                try:
                    iterable.close()
                except Exception as e:
                    request = self.build_request(environ)
                    self.sender.send_exception(exception=e, request=request)
                    raise

    def build_request(self, environ):
        request = {}

        http_host = environ.get('HTTP_HOST'], None)
        if http_host is not None:
            http_host = http_host.replace(' ', '')

        try:
            request = {
                'httpMethod': environ.get('REQUEST_METHOD', None),
                'url': environ.get('PATH_INFO', None),
                'ipAddress': environ.get('REMOTE_ADDR', None),
                'hostName': http_host
                'queryString': environ.get('QUERY_STRING', None),
                'headers': {},
                'form': {},
                'rawData': {}
            }
        except Exception:
            pass

        for key, value in environ.items():
            if key.startswith('HTTP_'):
               request['headers'][key] = value

        return request
