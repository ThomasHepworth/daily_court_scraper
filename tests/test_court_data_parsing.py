from datetime import datetime

import bs4
from src.scrapers.court_status_parsing import (
    CourtInfo,
    get_daily_court_table_info,
    parse_last_updated_datetime,
)


def test_get_daily_court_status_info(court_info_test_examples):
    court_info = get_daily_court_table_info(court_info_test_examples.table)
    assert isinstance(court_info, list)
    for info in court_info:
        assert isinstance(info, CourtInfo)
        assert isinstance(info.court_name, str)
        assert isinstance(info.table, bs4.element.Tag)


def test_court_info():
    random_court = CourtInfo(
        "Aylesbury", bs4.BeautifulSoup("<table></table>", "html.parser")
    )

    assert random_court.court_name == "Aylesbury"
    assert isinstance(random_court.table, bs4.element.Tag)


def test_parse_last_updated_datetime(court_info_test_examples):
    # Hacky solution, but we are expecting one of the following datetimes:
    expected_results_bucket = {
        "aylesbury": datetime.strptime(
            "Friday 22 November 2024 10:23", "%A %d %B %Y %H:%M"
        ),
        "barnstaple": datetime.strptime(
            "Friday 22 November 2024 10:42", "%A %d %B %Y %H:%M"
        ),
        "hove": datetime.strptime("Friday 22 November 2024 11:52", "%A %d %B %Y %H:%M"),
    }
    last_updated = parse_last_updated_datetime(
        court_info_test_examples.table.find("div", id="content-column")
    )
    court = court_info_test_examples.court_name.replace(".htm", "").lower()

    # TODO(ThomasHepworth): Clean up this test!
    assert last_updated == expected_results_bucket[court]


# def test_datetime_parse_error()
