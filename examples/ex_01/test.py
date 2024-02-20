from unittest import TestCase
from main import add_arguments

class TestCase01(TestCase):  # <- TestCase

    def test_add_numbers(self):  # <- Must start with "test"
        return_value = add_arguments(1, 2)
        self.assertEqual(return_value, 3)  # <- Custom assert method

