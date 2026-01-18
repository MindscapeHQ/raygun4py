import unittest
from unittest import mock

import flask
from raygun4py.middleware.flask import Provider


class TestFlaskMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app.config["TESTING"] = True
        self.provider = Provider(self.app, "test_api_key")
        self.provider.attach()

    def test_provider_registered_as_extension(self):
        self.assertIn("raygun", self.app.extensions)
        self.assertIs(self.app.extensions["raygun"], self.provider)

    def test_attach_creates_sender(self):
        self.assertIsNotNone(self.provider.sender)

    def test_get_flask_environment(self):
        env = self.provider._get_flask_environment()
        self.assertEqual(env["frameworkVersion"], f"Flask {flask.__version__}")

    def test_send_exception_calls_sender(self):
        self.provider.sender.send_exception = mock.MagicMock(return_value=True)

        try:
            raise ValueError("test error")
        except ValueError:
            import sys

            self.provider.send_exception(exc_info=sys.exc_info())

        self.provider.sender.send_exception.assert_called_once()

    def test_send_exception_without_attach_logs_error(self):
        provider = Provider(self.app, "test_api_key")

        with mock.patch("raygun4py.middleware.flask.log") as mock_log:
            provider.send_exception(exception=Exception("test"))
            mock_log.error.assert_called_once()

    def test_send_exception_merges_extra_environment_data(self):
        self.provider.sender.send_exception = mock.MagicMock(return_value=True)

        try:
            raise ValueError("test error")
        except ValueError:
            import sys

            self.provider.send_exception(
                exc_info=sys.exc_info(),
                extra_environment_data={"custom_key": "custom_value"},
            )

        call_kwargs = self.provider.sender.send_exception.call_args[1]
        self.assertIn("extra_environment_data", call_kwargs)
        self.assertEqual(
            call_kwargs["extra_environment_data"]["custom_key"], "custom_value"
        )
        self.assertIn("frameworkVersion", call_kwargs["extra_environment_data"])

    def test_exception_signal_triggers_send(self):
        self.provider.sender.send_exception = mock.MagicMock(return_value=True)

        @self.app.route("/error")
        def error_route():
            raise ValueError("test error")

        with self.app.test_client() as client:
            try:
                client.get("/error")
            except ValueError:
                pass

        self.provider.sender.send_exception.assert_called_once()

    def test_config_passed_to_sender(self):
        app = flask.Flask(__name__)
        config = {"transmitLocalVariables": False}
        provider = Provider(app, "test_api_key", config=config)
        sender = provider.attach()

        self.assertFalse(sender.transmit_local_variables)
