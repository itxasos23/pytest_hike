from unittest import TestCase
from main import get_random_cat_fact

class TestCase02(TestCase):  

    def test_random_cat_fact(self):
        return_value = get_random_cat_fact()

        self.assertTrue(len(return_value) > 0)  

