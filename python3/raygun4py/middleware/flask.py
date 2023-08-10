import logging

import flask
from flask.signals import got_request_exception

from raygun4py import raygunprovider

log = logging.getLogger(__name__)


class Provider(object):
    def __init__(self, flaskApp, apiKey, config=None):
        self.flaskApp = flaskApp
        self.apiKey = apiKey
        self.config = config if config is not None else {}
        self.sender = None

        got_request_exception.connect(self.send_exception, sender=flaskApp)

        flaskApp.extensions['raygun'] = self

    def attach(self):
        if not hasattr(self.flaskApp, 'extensions'):
            self.flaskApp.extensions = {}

        self.sender = raygunprovider.RaygunSender(
            self.apiKey, config=self.config)
        return self.sender

    def send_exception(self, exception=None, exc_info=None, user=None, **kwargs):
        """
        Send an exception report to Raygun. This middleware method enhances the report with Flask-specific environment data before sending.

        One of the parameters 'exception' or 'exc_info' must be non-None to send a valid exception report.

        Parameters:
            exception (Exception, optional): An exception instance to report.
            exc_info (tuple, optional): A 3-tuple containing exception type, exception instance, and traceback.
            user (dict or str, optional): Information about the affected user.
            tags (list, optional): A list of tags relating to the current context which you can define.
            userCustomData (dict, optional): A dictionary containing custom key-values also of your choosing.
            httpRequest (dict, optional): HTTP Request data that you wish to include with the report.

        Returns:
            The result of the post request, typically indicating the success or failure of the exception report transmission.
        """
        if not self.sender:
            log.error("Raygun-Flask: cannot send as provider not attached!")
            return

        env = self._get_flask_environment()
        # Ensure extra_environment_data is merged or added
        if 'extra_environment_data' in kwargs:
            kwargs['extra_environment_data'].update(env)
        else:
            kwargs['extra_environment_data'] = env

        self.sender.send_exception(
            exception=exception, exc_info=exc_info, user_override=user, **kwargs)

    def _get_flask_environment(self):
        return {
            'frameworkVersion': 'Flask ' + getattr(flask, '__version__', '')
        }
