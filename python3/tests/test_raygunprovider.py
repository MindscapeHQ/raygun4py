import logging
import sys
import unittest
from unittest import mock

from raygun4py import __version__, raygunmsgs, raygunprovider, utilities
from raygun4py import version as version_file


class TestRaygunSender(unittest.TestCase):
    def setUp(self):
        self.sender = raygunprovider.RaygunSender("invalidapikey")
        self.handler = raygunprovider.RaygunHandler("testkey", "v1.0")

    def test_apikey(self):
        self.assertEqual(self.sender.api_key, "invalidapikey")

    def test_handler_apikey(self):
        self.assertEqual(self.handler.sender.api_key, "testkey")

    def test_handler_version(self):
        self.assertEqual(self.handler.version, "v1.0")

    def test_sending_403_with_invalid_key(self):
        try:
            raise Exception("test")
        except Exception:
            info = sys.exc_info()
            http_result = self.sender.send_exception(exc_info=info)
            self.assertEqual(http_result[0], 403)

    def test_ignore_exceptions(self):
        ex = ["Exception"]
        self.sender.ignore_exceptions(ex)

        self.assertEqual(self.sender.ignored_exceptions, ex)

    def test_filter_keys_set(self):
        keys = ["credit_card"]
        self.sender.filter_keys(keys)

        self.assertEqual(self.sender.filtered_keys, keys)

    def test_filter_keys_filters_error(self):
        keys = ["identifier"]
        self.sender.filter_keys(keys)

        self.sender.set_user({"identifier": "foo"})

        self.assertEqual(
            utilities.filter_keys(keys, self.sender.user)["identifier"], "<filtered>"
        )

    def test_set_transmitLocalVariables(self):
        self.sender = raygunprovider.RaygunSender(
            "foo", config={"transmit_local_variables": False}
        )

        self.assertFalse(self.sender.transmit_local_variables)

    def test_set_transmitLocalVariables_camelcase(self):
        self.sender = raygunprovider.RaygunSender(
            "foo", config={"transmitLocalVariables": False}
        )
        self.assertFalse(self.sender.transmit_local_variables)

    def test_default_transmitLocalVariables(self):
        self.sender = raygunprovider.RaygunSender("foo")

        self.assertTrue(self.sender.transmit_local_variables)

    def test_set_transmit_global_variables(self):
        self.sender = raygunprovider.RaygunSender(
            "foo", config={"transmit_global_variables": False}
        )
        self.assertFalse(self.sender.transmit_global_variables)

    def test_set_transmit_global_variables_camelcase(self):
        self.sender = raygunprovider.RaygunSender(
            "foo", config={"transmitGlobalVariables": False}
        )
        self.assertFalse(self.sender.transmit_global_variables)

    def test_default_global_variables(self):
        self.sender = raygunprovider.RaygunSender("foo")
        self.assertTrue(self.sender.transmit_global_variables)

    def test_module_version_matches(self):
        self.assertEqual(__version__, version_file.__version__)


class TestCreateMessage(unittest.TestCase):
    def test_merge_tags(self):
        sender = raygunprovider.RaygunSender("apikey")
        sender.set_tags(["Tag1"])
        message = sender._create_message(
            raygunExceptionMessage=None,
            user_custom_data=None,
            http_request=None,
            extra_environment_data=None,
            user_override=None,
            tags=["Tag2"],
        )
        self.assertEqual(message.get_details()["tags"], ["Tag1", "Tag2"])

    def test_merge_custom_data(self):
        sender = raygunprovider.RaygunSender("apikey")
        sender.set_customdata({"CustomData1": "Value1"})
        message = sender._create_message(
            raygunExceptionMessage=None,
            user_custom_data={"CustomData2": "Value2"},
            http_request=None,
            extra_environment_data=None,
            user_override=None,
            tags=None,
        )
        self.assertEqual(
            message.get_details()["userCustomData"],
            {"CustomData1": "Value1", "CustomData2": "Value2"},
        )


class TestGroupingKey(unittest.TestCase):
    def the_callback(self, raygun_message):
        return self.key

    def the_callback_with_error(self, raygun_message):
        return raygun_message.get_error().message[:100]

    def create_dummy_message(self):
        self.sender = raygunprovider.RaygunSender("apikey")

        msg = raygunmsgs.RaygunMessageBuilder({}).new()
        errorMessage = raygunmsgs.RaygunErrorMessage(Exception, None, None, {})
        msg.set_exception_details(errorMessage)
        return msg.build()

    def test_message_with_error(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback_with_error)
        msg = self.sender._transform_message(msg)
        self.assertEqual(msg.get_details()["groupingKey"], "Exception: None")

    def test_groupingkey_is_not_none_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = "foo"
        msg = self.sender._transform_message(msg)

        self.assertIsNotNone(msg.get_details()["groupingKey"])

    def test_groupingkey_is_set_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = "foo"
        msg = self.sender._transform_message(msg)

        self.assertEqual(msg.get_details()["groupingKey"], "foo")

    def test_groupingkey_is_string_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = "foo"
        msg = self.sender._transform_message(msg)

        self.assertIsInstance(msg.get_details()["groupingKey"], str)

    def test_groupingkey_is_none_when_not_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = object
        msg = self.sender._transform_message(msg)

        self.assertIsNone(msg.get_details()["groupingKey"])

    def test_groupingkey_is_none_when_empty_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = ""
        msg = self.sender._transform_message(msg)

        self.assertIsNone(msg.get_details()["groupingKey"])

    def test_groupingkey_is_set_when_ok_length_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = "a"

        for i in range(0, 99):
            self.key += "a"

        msg = self.sender._transform_message(msg)
        self.assertEqual(msg.get_details()["groupingKey"], self.key)

    def test_groupingkey_is_none_when_too_long_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = "a"

        for i in range(0, 100):
            self.key += "a"

        msg = self.sender._transform_message(msg)
        self.assertIsNone(msg.get_details()["groupingKey"])


class TestRaygunHandler(unittest.TestCase):
    def setUp(self):
        self.handler = raygunprovider.RaygunHandler("testkey", "v1.0")
        self.handler.sender.send_exception = mock.MagicMock(return_value=(202, "OK"))

    def test_logging_outside_exception_context(self):
        """Test that RaygunHandler can handle logging outside of an exception context"""
        logger = logging.getLogger("test_logger")
        logger.addHandler(self.handler)

        # Log a message without an exception context
        logger.error("Test error message")

        # Verify that send_exception was called with a fallback error
        self.handler.sender.send_exception.assert_called_once()
        call_args = self.handler.sender.send_exception.call_args[1]
        self.assertIsNotNone(call_args.get("fallback_error"))
        self.assertEqual(call_args.get("tags"), ["Error Log"])

        logger.removeHandler(self.handler)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
