from unittest import TestCase
from unittest import mock

from main import get_random_cat_fact

class TestCase02Mocked(TestCase):  
    
    def setUp(self):
        self.mock_requests_patch = mock.patch("main.requests")
        print(self.mock_requests_patch)
        self.mock_requests_object = self.mock_requests_patch.start() # mock starts
        print(self.mock_requests_object)

    def test_add_numbers(self):
        # We set requests.get().json()'s return value
        self.mock_requests_object.get.return_value.json.return_value = {"fact": "Cats are amazing!"}

        return_value = get_random_cat_fact()

        self.assertEqual(return_value, "Cats are amazing!")

    def tearDown(self):
        self.mock_requests_patch.stop() # mock stops

