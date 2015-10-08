from raygun4py import raygunprovider

class Provider(object):

    def __init__(self, app, apiKey, config=None):
        self.app = app
        self.sender = raygunprovider.RaygunSender(apiKey, config or {})

    def __call__(self, environ, start_response):
        if not self.sender:
            print >> sys.stderr, ("Raygun-WSGI: Cannot send as provider not attached")

        try:
            chunk = self.app(environ, start_response)
        except Exception as e:
            request = self.build_request(environ)
            self.sender.send_exception(exception=e, request=request)

            raise

        try:
            for event in chunk:
                yield event
        except Exception as e:
            request = build_request(environ)
            self.sender.send_exception(exception=e, request=request)

            raise
        finally:
            if chunk and hasattr(chunk, 'close') and callable(chunk.close):
                try:
                    chunk.close()
                except Exception as e:
                    request = build_request(environ)
                    self.send_exception(exception=e, request=request)

    def build_request(self, environ):
        request = {}

        try:
            request = {
                'httpMethod': environ['REQUEST_METHOD'],
                'url': environ['PATH_INFO'],
                'ipAddress': environ['REMOTE_ADDR'],
                'hostName': environ['HTTP_HOST'].replace(' ', ''),
                'queryString': environ['QUERY_STRING'],
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
