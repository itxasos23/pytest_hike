from main import get_random_cat_fact

def test_add_numbers(mock_requests):
    mock_requests.get.return_value.json.return_value = {"fact": "Cats are amazing!"}
    return_value = get_random_cat_fact()
    assert return_value == "Cats are amazing!"
