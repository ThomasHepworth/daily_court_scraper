from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Generator, List, NamedTuple

import dlt
from pydantic import BaseModel

from src.scrapers.scraper import sanitise_text
from src.scrapers.validation import _validate_table_headers

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class CourtEndpoint(NamedTuple):
    court_region: str
    endpoint_suffix: str

    @property
    def endpoint_url(self) -> str:
        """
        Generate the full endpoint URL based on the endpoint suffix.
        """
        base_url = dlt.config.get("api.base_url")
        return f"{base_url}/{self.endpoint_suffix}"

    def __repr__(self) -> str:
        return f"{self.court_region} - {self.endpoint_url}"


class CourtInfo(NamedTuple):
    court_name: str
    table: BeautifulSoup


# TODO(ThomasHepworth): Add validation for the CourtData model.
class CourtRoomData(BaseModel):
    court_number: str
    case_number: str
    defendant_name: str
    trial_status: str

    @classmethod
    def from_html_row(cls, table_row: BeautifulSoup) -> CourtRoomData:
        """
        Parses a BeautifulSoup <tr> element to create a CourtData instance.
        """
        try:
            row_contents = table_row.find_all("td")
            return cls(
                court_number=sanitise_text(row_contents[0].get_text(strip=True)),
                case_number=sanitise_text(row_contents[1].get_text(strip=True)),
                defendant_name=split_defendant_name(row_contents[2]),
                trial_status=sanitise_text(row_contents[3].get_text(strip=True)),
            )
        except IndexError as e:
            raise ValueError(
                f"Invalid table row structure: {table_row}. Expected 4 <td> elements."
            ) from e

    def dict(self, **kwargs) -> Dict[str, Any]:
        """
        Returns the model as a dictionary with optionally custom serialisation.
        Overrides BaseModel's `dict()` method to handle non-serialisable fields or
        rename keys.
        """
        return super().model_dump(**kwargs)


def parse_last_updated_datetime(page_contents: BeautifulSoup) -> str:
    weekdays = {
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    }
    potential_datetime_str = page_contents.find_all("p")
    for p_tag in potential_datetime_str:
        datetime_str = p_tag.text
        if datetime_str.split(" ")[0].lower() in weekdays:
            return datetime.strptime(datetime_str, "%A %d %B %Y %H:%M")

    raise ValueError("Could not find a valid datetime string in <p> tags.")


def split_defendant_name(defendant_contents: BeautifulSoup) -> str:
    """
    Parses defendant contents, collapsing <br> or similar tags into a single,
    semicolon-delimited string of sanitised names.

    Args:
        defendant_contents (BeautifulSoup): HTML content containing defendant names.

    Returns:
        str: Semicolon-delimited string of defendant names.
    """
    if not defendant_contents or not defendant_contents.text.strip():
        return ""

    # Extract and sanitise text, ignoring non-string elements
    defendant_names = [
        sanitise_text(str(content))
        for content in defendant_contents.contents
        if isinstance(content, str)
    ]

    return ";".join(name for name in defendant_names if name)


def get_daily_court_table_info(
    page_contents: BeautifulSoup,
) -> Generator[CourtInfo, None, None]:
    """
    Generator function to extract court table data from the page.

    Args:
        page_contents (BeautifulSoup): Parsed HTML page contents.

    Yields:
        CourtInfo: An object containing the h2 text and associated table data.
    """
    for table in page_contents.find_all("table"):
        h2 = table.find_previous_sibling("h2")
        if h2:
            yield CourtInfo(h2.text.strip(), table)
        else:
            raise ValueError("Could not find a valid h2 tag.")


@_validate_table_headers(dlt.config.get("api.court_table_headers"))
def process_court_rows(court_info: CourtInfo) -> Generator[CourtRoomData, None, None]:
    for table_contents in court_info.table.find_all("tr")[1:]:
        row_data: CourtRoomData = CourtRoomData.from_html_row(table_contents)

        yield {
            "court_name": court_info.court_name,
            **row_data.dict(),
        }


def process_court_info(
    court_region: str, last_updated_datetime: str, webpage_contents: BeautifulSoup
) -> Generator[dict, None, None]:
    for court_info in get_daily_court_table_info(webpage_contents):
        for processed_row in process_court_rows(court_info):
            yield {
                "court_region": court_region,
                "last_updated_timestamp": last_updated_datetime,
                **processed_row,
            }
