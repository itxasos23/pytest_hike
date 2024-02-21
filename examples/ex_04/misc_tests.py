import pytest
import os
import logging
from icecream import ic
from main import get_random_cat_fact

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("root")


@pytest.mark.parametrize("test_input, expected", [(1, 2), (2, 4), (3, 6)])
def test_double(test_input, expected):
    assert test_input * 2 == expected


def test_env(monkeypatch):
    assert os.getenv("BEST_SINGER") is None

    monkeypatch.setenv("BEST_SINGER", "Hatsune Miku")
    assert os.getenv("BEST_SINGER") == "Hatsune Miku"

    monkeypatch.setenv("BEST_SINGER", "Tracy Chapman")
    assert os.getenv("BEST_SINGER") == "Tracy Chapman"

def test_log_assert(caplog):
    logger.warning("Hey Link!")
    ic(caplog.text)
    ic(caplog.records)
    assert "Link" in caplog.text

def test_get_random_cat_fact(mock_requests):
    mock_requests.get.return_value.json.return_value = {"fact": "Cats are amazing!"}
    return_value = get_random_cat_fact()
    assert return_value == "Cats are amazing!"

    # We assert that the mock was called with what we expect.
    mock_requests.get.assert_called_with("https://catfact.ninja/fact")
    mock_requests.get.return_value.json.assert_called_with()
    ic(mock_requests.get.call_args_list)
    ic(mock_requests.get.return_value.json.call_args_list)


