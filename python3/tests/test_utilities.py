import unittest

from raygun4py import utilities


class TestRaygunUtilities(unittest.TestCase):
    def test_filter_keys(self):
        test_obj = {"foo": "bar", "baz": "qux"}

        test_obj = utilities.filter_keys(["foo"], test_obj)

        self.assertEqual(test_obj["foo"], "<filtered>")

    def test_filter_keys_recursive(self):
        test_obj = {"foo": "bar", "baz": "qux", "boo": {"foo": "qux"}}

        test_obj = utilities.filter_keys(["foo"], test_obj)

        self.assertEqual(test_obj["foo"], "<filtered>")
        self.assertEqual(test_obj["boo"]["foo"], "<filtered>")

    def test_filter_keys_start(self):
        test_obj = {"foobar": "bar", "barfoobar": "baz", "barfoo": "qux", "foo": "bar"}

        test_obj = utilities.filter_keys(["foo*"], test_obj)

        self.assertEqual(test_obj["foobar"], "<filtered>")
        self.assertEqual(test_obj["barfoobar"], "baz")
        self.assertEqual(test_obj["barfoo"], "qux")
        self.assertEqual(test_obj["foo"], "<filtered>")

    def test_filter_keys_end(self):
        test_obj = {"foobar": "bar", "barfoobar": "baz", "barfoo": "qux", "foo": "bar"}

        test_obj = utilities.filter_keys(["*foo"], test_obj)

        self.assertEqual(test_obj["foobar"], "bar")
        self.assertEqual(test_obj["barfoobar"], "baz")
        self.assertEqual(test_obj["barfoo"], "<filtered>")
        self.assertEqual(test_obj["foo"], "<filtered>")

    def test_filter_keys_any(self):
        test_obj = {"foobar": "bar", "barfoobar": "baz", "barfoo": "qux", "foo": "bar"}

        test_obj = utilities.filter_keys(["*foo*"], test_obj)

        self.assertEqual(test_obj["foobar"], "<filtered>")
        self.assertEqual(test_obj["barfoobar"], "<filtered>")
        self.assertEqual(test_obj["barfoo"], "<filtered>")
        self.assertEqual(test_obj["foo"], "<filtered>")

    def test_filter_keys_exact(self):
        test_obj = {"foobar": "bar", "barfoobar": "baz", "barfoo": "qux", "foo": "bar"}

        test_obj = utilities.filter_keys(["foo"], test_obj)

        self.assertEqual(test_obj["foobar"], "bar")
        self.assertEqual(test_obj["barfoobar"], "baz")
        self.assertEqual(test_obj["barfoo"], "qux")
        self.assertEqual(test_obj["foo"], "<filtered>")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
