from chaosazure import credentials
import unittest


def test_create_from_with_empty_secrets():
    credentials.create_from(None)


class ExampleTest(unittest.TestCase):
    def test_error(self):
        with self.assertRaises(Exception):
            test_create_from_with_empty_secrets()
