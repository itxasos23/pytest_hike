from unittest import TestCase

class TestCase03(TestCase):  

    def test_greater(self):
        self.assertGreater(3, 4)

    def test_greater_assert(self):
        assert 3 > 4

    def test_introspection(self):
        dict_1 = {"key_1": "value_1"}
        dict_2 = {"key_1": "value_2"}

        assert dict_1 == dict_2
