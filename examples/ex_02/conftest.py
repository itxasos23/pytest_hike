from unittest import mock
import pytest

@pytest.fixture
def mock_requests():
    with mock.patch("main.requests") as mock_requests:
        yield mock_requests
