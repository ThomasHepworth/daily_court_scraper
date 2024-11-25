from typing import Generator

from src.scrapers.court_data import (
    CourtEndpoint,
    parse_last_updated_datetime,
    process_court_info,
)
from src.scrapers.scraper import (
    fetch_webpage_html,
    sanitise_text,
)


def scrape_court_data(court: CourtEndpoint) -> Generator[dict, None, None]:
    webpage_contents = fetch_webpage_html(court.endpoint_url).find(
        "div", id="content-column"
    )
    last_updated_datetime = parse_last_updated_datetime(webpage_contents)
    yield from process_court_info(
        court.court_region, last_updated_datetime, webpage_contents
    )


__all__ = ["scrape_court_data", "fetch_webpage_html", "sanitise_text", "CourtEndpoint"]
