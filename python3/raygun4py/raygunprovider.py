import copy
import logging
import socket
import sys

import jsonpickle
import requests

from raygun4py import raygunmsgs, utilities

DEFAULT_CONFIG = {
    "before_send_callback": None,
    "grouping_key_callback": None,
    "filtered_keys": [],
    "ignored_exceptions": [],
    "proxy": None,
    "transmit_global_variables": True,
    "transmit_local_variables": True,
    "enforce_payload_size_limit": True,
    "log_payload_size_limit_breaches": True,
    "transmit_environment_variables": True,
    "userversion": "Not defined",
    "user": None,
    "http_timeout": 10.0,
}


class RaygunSender:
    """
    A sender for reporting errors to Raygun.

    Attributes:
        api_key (str): The API key for Raygun.
    """

    log = logging.getLogger(__name__)

    api_key = None
    endpointprotocol = "https://"
    endpointhost = "api.raygun.io"
    endpointpath = "/entries"
    process_tags = []
    process_custom_data = dict()

    def __init__(self, api_key, config={}):
        """
        Initialize a RaygunSender.

        Parameters:
            api_key (str): The API key for Raygun.
            config (dict, optional): Configuration options. Defaults to an empty dictionary.
        """
        if api_key:
            if not isinstance(api_key, str):
                self.log.error(
                    f"Expected api_key of type str, but got {type(api_key).__name__}. Errors will not be transmitted."
                )
                self.api_key = None
            else:
                self.api_key = api_key
        else:
            self.log.warning(
                "RaygunProvider error: api_key not set, errors will not be transmitted."
            )

        try:
            import ssl  # noqa: F401
        except ImportError:
            self.log.warning(
                "RaygunProvider error: No SSL support available, cannot send. Please"
                "compile the socket module with SSL support."
            )

        # Set up the default values
        default_config = utilities.snakecase_dict(copy.deepcopy(DEFAULT_CONFIG))
        default_config.update(utilities.snakecase_dict(config or {}))
        for k, v in default_config.items():
            setattr(self, k, v)

    def set_version(self, version):
        """
        Set the version for the error reports.

        Parameters:
            version (str): Version string.
        """
        if isinstance(version, str):
            self.userversion = version

    def set_user(self, user):
        """
        Set user information for the error reports.

        Parameters:
            user: User information.
        """
        self.user = user

    def set_tags(self, tags):
        """
        Set tags for the error reports.

        Parameters:
            tags (list): List of tags.
        """
        if type(tags) is list:
            self.process_tags = tags

    def set_customdata(self, custom_data):
        if type(custom_data) is dict:
            self.process_custom_data = custom_data

    def ignore_exceptions(self, exceptions):
        """
        Set exceptions that should be ignored.

        Parameters:
            exceptions (list): List of exceptions to ignore.
        """
        if isinstance(exceptions, list):
            self.ignored_exceptions = exceptions

    def filter_keys(self, keys):
        """
        Set keys to be filtered out from the error reports.

        Parameters:
            keys (list): List of keys to filter out.
        """
        if isinstance(keys, list):
            self.filtered_keys = keys

    def set_proxy(self, host, port):
        """
        Set a proxy for the sender.

        Parameters:
            host (str): Proxy host.
            port (int): Proxy port.
        """
        self.proxy = {"host": host, "port": port}

    def on_before_send(self, callback):
        """
        Set a callback to be executed before sending a report.

        Parameters:
            callback (callable): Callback function to be executed.
        """
        if callable(callback):
            self.before_send_callback = callback

    def on_grouping_key(self, callback):
        """
        Set a callback to customize the grouping key for the report.

        Parameters:
            callback (callable): Callback function to customize grouping.
        """
        if callable(callback):
            self.grouping_key_callback = callback

    def send_exception(
        self, exception=None, exc_info=None, user_override=None, **kwargs
    ):
        """
        Send an exception report to Raygun.

        Parameters:
            exception (Exception, optional): An exception instance to report.
            exc_info (tuple, optional): A 3-tuple containing exception type, exception instance, and traceback.
            user_override (dict or str, optional): Information about the affected user. If not provided, 'self.user' will be used.
            tags (list, optional): A list of tags relating to the current context which you can define.
            userCustomData (dict, optional): A dictionary containing custom key-values also of your choosing.
            httpRequest (dict, optional): HTTP Request data that you wish to include with the report.

        Returns:
            The result of the post request, typically indicating the success or failure of the exception report transmission.
        """
        options = {
            "transmitLocalVariables": self.transmit_local_variables,
            "transmitGlobalVariables": self.transmit_global_variables,
            "enforce_payload_size_limit": self.enforce_payload_size_limit,
            "log_payload_size_limit_breaches": self.log_payload_size_limit_breaches,
        }
        (
            tags,
            custom_data,
            http_request,
            extra_environment_data,
            custom_message,
            fallback_error,
        ) = self._parse_args(kwargs)

        exc_type, exc_value, exc_traceback = exc_info or sys.exc_info()
        if fallback_error and not (exc_type or exception):
            errorMessage = fallback_error
        else:
            errorMessage = self._create_error_message(
                exception, exc_type, exc_value, exc_traceback, options, custom_message
            )

        message = self._create_message(
            errorMessage,
            tags,
            custom_data,
            http_request,
            extra_environment_data,
            user_override,
        )
        message = self._transform_message(message)

        if message is not None:
            return self._post(message)

    def _create_error_message(
        self,
        exception,
        exc_type,
        exc_value,
        exc_traceback,
        options,
        custom_message=None,
    ):
        if exception:
            return raygunmsgs.RaygunErrorMessage(
                type(exception),
                exception,
                exception.__traceback__,
                options,
                custom_message,
            )
        else:
            return raygunmsgs.RaygunErrorMessage(
                exc_type, exc_value, exc_traceback, options, custom_message
            )

    def _parse_args(self, kwargs):
        tags = kwargs["tags"] if "tags" in kwargs else None
        custom_data = kwargs["userCustomData"] if "userCustomData" in kwargs else None
        extra_environment_data = (
            kwargs["extra_environment_data"]
            if "extra_environment_data" in kwargs
            else None
        )
        custom_message = (
            kwargs["custom_message"] if "custom_message" in kwargs else None
        )
        fallback_error = (
            kwargs["fallback_error"] if "fallback_error" in kwargs else None
        )

        http_request = None
        if "httpRequest" in kwargs:
            http_request = kwargs["httpRequest"]
        elif "request" in kwargs:
            http_request = kwargs["request"]

        return (
            tags,
            custom_data,
            http_request,
            extra_environment_data,
            custom_message,
            fallback_error,
        )

    def _create_message(
        self,
        raygunExceptionMessage,
        tags,
        user_custom_data,
        http_request,
        extra_environment_data,
        user_override=None,
    ):
        options = {
            "transmit_environment_variables": self.transmit_environment_variables
        }
        return (
            raygunmsgs.RaygunMessageBuilder(options)
            .new()
            .set_machine_name(socket.gethostname())
            .set_version(self.userversion)
            .set_client_details()
            .set_exception_details(raygunExceptionMessage)
            .set_environment_details(extra_environment_data)
            .set_tags(self.process_tags)
            .set_tags(tags)
            .set_customdata(self.process_custom_data)
            .set_customdata(user_custom_data)
            .set_request_details(http_request)
            .set_user(user_override if user_override else self.user)
            .build()
        )

    def _transform_message(self, message):
        message = utilities.ignore_exceptions(self.ignored_exceptions, message)

        if message is not None:
            message = utilities.filter_keys(self.filtered_keys, message)
            message.get_details()["groupingKey"] = utilities.execute_grouping_key(
                self.grouping_key_callback, message
            )

        if self.before_send_callback is not None:
            mutated_payload = self.before_send_callback(message.get_details())

            if mutated_payload is not None:
                message.set_details(mutated_payload)
            else:
                return None

        return message

    def _post(self, raygunMessage):
        options = {
            "enforce_payload_size_limit": self.enforce_payload_size_limit,
            "log_payload_size_limit_breaches": self.log_payload_size_limit_breaches,
        }

        if (
            isinstance(raygunMessage.get_error(), raygunmsgs.RaygunErrorMessage)
            and "enforce_payload_size_limit" in options
            and options["enforce_payload_size_limit"] is True
        ):
            error = jsonpickle.loads(jsonpickle.dumps(raygunMessage.get_error()))

            error.check_and_modify_payload_size(options)

            raygunMessage.set_error(error)

        json = jsonpickle.encode(raygunMessage, unpicklable=False)

        try:
            headers = {
                "X-ApiKey": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "raygun4py",
            }

            response = requests.post(
                self.endpointprotocol + self.endpointhost + self.endpointpath,
                headers=headers,
                data=json,
                timeout=self.http_timeout,
            )
        except Exception as e:
            self.log.error(e)
            return 400, "Exception: Could not send"
        return response.status_code, response.text


class RaygunHandler(logging.Handler):
    """
    Logging handler for sending error logs to Raygun.

    Attributes:
        sender (RaygunSender): The RaygunSender to use for sending.
        version (str): Version for the RaygunSender.
    """

    def __init__(self, api_key=None, version=None, level=logging.ERROR, sender=None):
        """
        Initialize a RaygunHandler for logging.

        For constructing instances using an existing RaygunSender, it is recommended to use the `RaygunHandler.from_sender()` class method.

        Parameters:
            api_key (str): The API key for Raygun.
            version (str, optional): Version for the RaygunSender. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.ERROR.
        """
        super().__init__(level)
        if api_key:
            self.sender = RaygunSender(api_key)
            if version:
                self.sender.set_version(version)
            self.version = version
        elif sender:
            self.sender = sender
            self.version = sender.userversion
        else:
            raise ValueError("Either 'api_key' or 'sender' must be provided.")

    @classmethod
    def from_sender(cls, sender, level=logging.ERROR):
        """
        Construct a RaygunHandler instance using an existing RaygunSender object.

        Parameters:
            sender (RaygunSender): The RaygunSender to use for sending.
            level (int, optional): Logging level. Defaults to logging.ERROR.

        Returns:
            RaygunHandler: A new instance of RaygunHandler.
        """
        if not isinstance(sender, RaygunSender):
            raise TypeError(
                f"Expected sender of type RaygunSender, but got {type(sender).__name__}"
            )
        return cls(level=level, sender=sender)

    def emit(self, record):
        # Use log level as a tag
        tag = self.get_tag_from_levelname(record.levelname)
        tags = [tag] if tag else []

        if record.exc_info:
            # exc_info was provided, so send it
            userCustomData = {
                "Logger Name": record.name,
            }
            self.sender.send_exception(
                exc_info=record.exc_info,
                userCustomData=userCustomData,
                tags=tags,
                custom_message=record.getMessage(),
            )
        else:
            # Proide a fallback error to use if exc_info cannot be obtained from sys
            fallback_error = raygunmsgs.RaygunLoggerFallbackErrorMessage(
                record.name,
                record.getMessage(),
                record.filename,
                record.funcName,
                record.lineno,
            )
            self.sender.send_exception(tags=tags, fallback_error=fallback_error)

    @staticmethod
    def get_tag_from_levelname(levelname):
        tag_map = {
            "DEBUG": "Debug Log",
            "INFO": "Info Log",
            "WARNING": "Warning Log",
            "ERROR": "Error Log",
            "CRITICAL": "Critical Log",
        }
        return tag_map.get(levelname)
