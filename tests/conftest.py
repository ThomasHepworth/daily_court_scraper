from typing import Tuple
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from src.scrapers.court_data import CourtInfo
from tests.helpers import TEST_DATA_DIR, dummy_court_bs4_files, read_local_html


@pytest.fixture(scope="session", params=dummy_court_bs4_files())
def court_test_example_html(request) -> BeautifulSoup:
    return read_local_html(request.param)


# TODO: This is invalid - it returns a CourtInfo, not the HTML
@pytest.fixture(scope="session", params=dummy_court_bs4_files())
def court_info_test_examples(request) -> Tuple[str, BeautifulSoup]:
    file = request.param
    court_name = file.removesuffix(".html").split("/")[-1].capitalize()
    return CourtInfo(court_name, read_local_html(file))


def mock_fetch_webpage(url: str) -> BeautifulSoup:
    url = url.replace("http://xhibit.justice.gov.uk/", TEST_DATA_DIR)
    return read_local_html(url)


@pytest.fixture(autouse=True)
def patch_fetch_webpage():
    """
    Patch `_fetch_webpage` to use `read_local_html` for all tests.
    """
    with patch(
        "src.scrapers.scraper.fetch_webpage_html", side_effect=mock_fetch_webpage
    ):
        yield
