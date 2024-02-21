import pytest
from unittest import mock

@pytest.fixture
def mock_requests():
    with mock.patch("main.requests") as mock_requests:
        yield mock_requests
