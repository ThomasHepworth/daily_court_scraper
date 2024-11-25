import logging
import re

import dlt
import requests
from bs4 import BeautifulSoup

from src._exceptions import FetchWebpageError
from src.scrapers.validation import _validate_xhibit_html

logger = logging.getLogger(__name__)


@_validate_xhibit_html(dlt.config.get("api.base_url"))
def fetch_webpage_html(url: str) -> requests.Response:
    session = requests.Session()  # Reuse session for connection pooling

    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch the webpage at {url}: {e}")
        raise FetchWebpageError(f"Could not fetch the webpage at {url}") from e

    return BeautifulSoup(response.content, "html.parser")


def sanitise_text(text: str) -> str:
    # Replace multiple spaces, tabs, or newlines with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove any carriage return characters (if any)
    text = text.replace("\r", "")

    # Strip leading and trailing whitespace
    return text.strip()
