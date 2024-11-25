from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from .court_data import CourtInfo

from .._exceptions import InvalidTableHeadersError

logger = logging.getLogger(__name__)


def _validate_table_headers(expected_headers: List[str]):
    """
    Decorator to validate table headers against an expected list.

    Args:
        expected_headers (List[str]): The list of expected headers.

    Returns:
        Callable: A decorator that validates headers for the decorated function.

    Raises:
        InvalidTableHeadersError: If the actual headers do not match the expected headers.
    """

    # TODO(ThomasHepworth): Clean up this logic - duplication of extraction
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(court_info: CourtInfo, *args, **kwargs):
            # Extract table headers
            tr_tag = court_info.table.find_next("tr")
            if not tr_tag:
                error_msg = "Header validation failed. No <tr> tag found in the table."
                logger.error(error_msg)
                raise InvalidTableHeadersError(error_msg)

            th_tags = tr_tag.find_all("th")
            if not th_tags:
                error_msg = (
                    "Header validation failed. No <th> tags found in the table row."
                )
                logger.error(error_msg)
                raise InvalidTableHeadersError(error_msg)

            headers = [header.text.strip() for header in th_tags]

            # Validate headers
            if headers != expected_headers:
                error_msg = (
                    f"Header validation failed. Expected headers: {expected_headers}, "
                    f"but received: {headers}."
                )
                logger.error(error_msg)
                raise InvalidTableHeadersError(error_msg)

            return func(court_info, *args, **kwargs)

        return wrapper

    return decorator


def _validate_xhibit_html(expected_url: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(url: str, *args, **kwargs):
            if not url.startswith(expected_url):
                error_msg = (
                    f"URL validation failed. Expected URL to start with: {expected_url}, "
                    f"but received: {url}."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            return func(url, *args, **kwargs)

        return wrapper

    return decorator
