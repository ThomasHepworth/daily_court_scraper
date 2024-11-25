import os
from bs4 import BeautifulSoup
from src.scrapers.scraper import fetch_webpage_html

from functools import lru_cache

TEST_DATA_DIR = "tests/test_data/"


def write_page_contents_to_file(page_contents: BeautifulSoup, filename: str) -> None:
    """
    Writes the contents of a BeautifulSoup object to a file.

    Args:
        page_contents (BeautifulSoup): The parsed HTML content.
        filename (str): The name of the file to write to.

    Raises:
        ValueError: If the provided page_contents is not a BeautifulSoup object.
    """
    if not isinstance(page_contents, BeautifulSoup):
        raise ValueError("page_contents must be a BeautifulSoup object.")

    # Convert BeautifulSoup object to a string
    content_as_string = str(page_contents)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content_as_string)


def write_courts_to_html(
    write_location: str = TEST_DATA_DIR, file_type: str = "html"
) -> None:
    # To run: write_courts_to_html(TEST_DATA_DIR, "htm")
    if file_type not in {"html", "htm"}:
        raise ValueError("Invalid file type provided. Must be 'html' or 'htm'.")

    courts_to_scrape = [
        ("aylesbury", "http://xhibit.justice.gov.uk/aylesbury.htm"),
        ("barnstaple", "http://xhibit.justice.gov.uk/barnstaple.htm"),
        ("hove", "http://xhibit.justice.gov.uk/lewes.htm"),
    ]
    for court, url in courts_to_scrape:
        soup_response: BeautifulSoup = fetch_webpage_html(url)
        write_page_contents_to_file(
            soup_response, f"{write_location}{court}.{file_type}"
        )


@lru_cache(maxsize=1)
def dummy_court_bs4_files():
    return [
        os.path.join(TEST_DATA_DIR, file)
        for file in os.listdir(TEST_DATA_DIR)
        if file.endswith(".htm")
    ]


@lru_cache(maxsize=None)
def read_local_html(file_path: str) -> BeautifulSoup:
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    return soup
