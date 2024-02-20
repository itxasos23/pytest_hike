import pytest
import os
import logging
from icecream import ic

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
    assert "Link" in caplog.text

