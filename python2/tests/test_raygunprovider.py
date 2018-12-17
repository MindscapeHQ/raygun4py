import sys
import unittest2 as unittest
from raygun4py import raygunprovider
from raygun4py import raygunmsgs
from raygun4py import utilities
from raygun4py import __version__
from raygun4py import version as version_file

class TestRaygunSender(unittest.TestCase):

    def setUp(self):
        self.sender = raygunprovider.RaygunSender('invalidapikey')
        self.handler = raygunprovider.RaygunHandler('testkey', 'v1.0')

    def test_apikey(self):
        self.assertEqual(self.sender.api_key, 'invalidapikey')

    def test_handler_apikey(self):
        self.assertEqual(self.handler.sender.api_key, 'testkey')

    def test_handler_version(self):
        self.assertEqual(self.handler.version, 'v1.0')

    def test_sending_403_with_invalid_key(self):
        try:
            raise StandardError('test')
        except Exception as e:
            info = sys.exc_info()
            http_result = self.sender.send_exception(info)
            self.assertEqual(http_result[0], 403)

    def test_ignore_exceptions(self):
        ex = ['Exception']
        self.sender.ignore_exceptions(ex)

        self.assertEqual(self.sender.ignored_exceptions, ex)

    def test_filter_keys_set(self):
        keys = ['credit_card']
        self.sender.filter_keys(keys)

        self.assertEqual(self.sender.filtered_keys, keys)

    def test_filter_keys_filters_error(self):
        keys = ['identifier']
        self.sender.filter_keys(keys)

        self.sender.set_user({ 'identifier': 'foo' })

        self.assertEqual(utilities.filter_keys(keys, self.sender.user)['identifier'], '<filtered>')

    def test_set_transmitLocalVariables(self):
        self.sender = raygunprovider.RaygunSender('foo', config={ 'transmit_local_variables': False })
        self.assertFalse(self.sender.transmit_local_variables)

    def test_set_transmitLocalVariables_camelcase(self):
        self.sender = raygunprovider.RaygunSender('foo', config={ 'transmitLocalVariables': False })
        self.assertFalse(self.sender.transmit_local_variables)

    def test_default_transmitLocalVariables(self):
        self.sender = raygunprovider.RaygunSender('foo')

        self.assertTrue(self.sender.transmit_local_variables)

    def test_set_transmit_global_variables(self):
        self.sender = raygunprovider.RaygunSender('foo', config={ 'transmit_global_variables': False })
        self.assertFalse(self.sender.transmit_global_variables)

    def test_set_transmit_global_variables_camelcase(self):
        self.sender = raygunprovider.RaygunSender('foo', config={ 'transmitGlobalVariables': False })
        self.assertFalse(self.sender.transmit_global_variables)

    def test_default_global_variables(self):
        self.sender = raygunprovider.RaygunSender('foo')
        self.assertTrue(self.sender.transmit_global_variables)

    def test_module_version_matches(self):
        self.assertEqual(__version__, version_file.__version__)


class TestGroupingKey(unittest.TestCase):

    def the_callback(self, raygun_message):
        return self.key

    def create_dummy_message(self):
        self.sender = raygunprovider.RaygunSender('apikey')

        msg = raygunmsgs.RaygunMessageBuilder().new()
        errorMessage = raygunmsgs.RaygunErrorMessage(Exception, None, None, {})
        msg.set_exception_details(errorMessage)
        return msg.build()

    def test_groupingkey_is_not_none_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = 'foo'
        self.sender._transform_message(msg)

        self.assertIsNotNone(msg.get_details()['groupingKey'])

    def test_groupingkey_is_set_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = 'foo'
        self.sender._transform_message(msg)

        self.assertEquals(msg.get_details()['groupingKey'], 'foo')

    def test_groupingkey_is_string_with_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = 'foo'
        self.sender._transform_message(msg)

        self.assertIsInstance(msg.get_details()['groupingKey'], str)

    def test_groupingkey_is_none_when_not_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = object
        self.sender._transform_message(msg)

        self.assertIsNone(msg.get_details()['groupingKey'])

    def test_groupingkey_is_none_when_empty_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = ''
        self.sender._transform_message(msg)

        self.assertIsNone(msg.get_details()['groupingKey'])

    def test_groupingkey_is_set_when_ok_length_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = 'a'

        for i in range(0, 99):
            self.key += 'a'

        self.sender._transform_message(msg)
        self.assertEqual(msg.get_details()['groupingKey'], self.key)

    def test_groupingkey_is_none_when_too_long_string_returned_from_callback(self):
        msg = self.create_dummy_message()
        self.sender.on_grouping_key(self.the_callback)
        self.key = 'a'

        for i in range(0, 100):
            self.key += 'a'

        self.sender._transform_message(msg)
        self.assertIsNone(msg.get_details()['groupingKey'])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
