import logging

from raygun4py import http_utilities, raygunprovider

log = logging.getLogger(__name__)


class Provider(object):

    def __init__(self, app, apiKey, config=None):
        self.app = app
        self.config = config if config is not None else {}
        self.sender = raygunprovider.RaygunSender(apiKey, config=self.config)

    def __call__(self, environ, start_response):
        iterable = None
        try:
            iterable = self.app(environ, start_response)
            for event in iterable:
                yield event

        except Exception as e:
            if self.sender:
                try:
                    request = http_utilities.build_wsgi_compliant_request(
                        environ)
                    self.sender.send_exception(exception=e, request=request)
                except Exception as inner:
                    log.error("Raygun-WSGI: could not send exception!")
                    log.error(inner)
            else:
                log.error("Raygun-WSGI: cannot send as provider not attached!")
            raise

        finally:
            if hasattr(iterable, 'close'):
                try:
                    iterable.close()
                except Exception as e:
                    if self.sender:
                        try:
                            rg_request_details = http_utilities.build_wsgi_compliant_request(
                                environ)
                            self.sender.send_exception(
                                exception=e, request=rg_request_details)
                        except Exception as inner:
                            log.error(
                                "Raygun-WSGI: could not send exception on close!")
                            log.error(inner)
                    else:
                        log.error(
                            "Raygun-WSGI: cannot send on close as provider not attached!")
                    raise
