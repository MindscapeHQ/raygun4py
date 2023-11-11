import unittest, sys
import socket
import inspect

from raygun4py import utilities

class TestRaygunUtilities(unittest.TestCase):
    def test_filter_keys(self):
        test_obj = {
            'foo': 'bar',
            'baz': 'qux'
        }

        utilities.filter_keys(['foo'], test_obj)

        self.assertEqual(test_obj['foo'], '<filtered>')

    def test_filter_keys_recursive(self):
        test_obj = {
            'foo': 'bar',
            'baz': 'qux',
            'boo': {
                'foo': 'qux'
            }
        }

        utilities.filter_keys(['foo'], test_obj)

        self.assertEqual(test_obj['foo'], '<filtered>')
        self.assertEqual(test_obj['boo']['foo'], '<filtered>')

    def test_filter_keys_with_wildcard(self):
        test_obj = {
            'foobr': 'bar',
            'foobz': 'baz',
            'fooqx': 'foo',
            'afooqx': 'afoo',
            'baz': 'qux'
        }

        utilities.filter_keys(['foo*'], test_obj)

        self.assertEqual(test_obj['foobr'], '<filtered>')
        self.assertEqual(test_obj['foobz'], '<filtered>')
        self.assertEqual(test_obj['fooqx'], '<filtered>')
        self.assertEqual(test_obj['afooqx'], 'afoo')
        self.assertEqual(test_obj['baz'], 'qux')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
