import logging
from typing import TYPE_CHECKING, Any, Dict, Generator
from urllib.parse import urljoin

import dlt

from src._exceptions import InvalidCourtDataException
from src.scrapers import (
    CourtEndpoint,
    fetch_webpage_html,
    sanitise_text,
    scrape_court_data,
)

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


@dlt.resource(primary_key="court")
def extract_court_details() -> Generator[CourtEndpoint, None, None]:
    court_list_endpoint = urljoin(
        dlt.config.get("api.base_url"), dlt.config.get("api.court_list_endpoint")
    )

    soup_response: BeautifulSoup = fetch_webpage_html(court_list_endpoint)
    page_contents = soup_response.find("div", id="content-column")

    if not page_contents:
        raise ValueError("No content found for the given page.")

    for court in page_contents.find_all("li"):
        court_name = sanitise_text(court.text)
        link = court.find("a")

        if not link or not link.has_attr("href"):
            raise InvalidCourtDataException(court_name, court.prettify())

        endpoint_suffix = link["href"]
        logger.debug(
            f"Found court '{court_name}' with endpoint URL: '{endpoint_suffix}'"
        )

        court_endpoint = CourtEndpoint(court_name, endpoint_suffix)

        yield court_endpoint


@dlt.transformer(
    data_from=extract_court_details,
    write_disposition="replace",
    parallelized=True,
)
def court_room_details(
    court_endpoint: CourtEndpoint,
) -> Generator[Dict[str, Any], None, None]:
    logger.debug(f"`court_room_details` processing: {court_endpoint}")

    yield scrape_court_data(court_endpoint)
