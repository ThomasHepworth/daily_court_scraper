from src.scrapers.scraper import fetch_webpage_html


def test_fetch_webpage_html():
    soup_response = fetch_webpage_html("http://xhibit.justice.gov.uk/aylesbury.htm")
    assert soup_response.find("title").text == "XHIBIT: Aylesbury"
