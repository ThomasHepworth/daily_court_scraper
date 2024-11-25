class InvalidCourtDataException(Exception):
    def __init__(self, court_name: str, court_data: str):
        self.court_name = court_name
        self.court_data = court_data
        super().__init__(
            f"Invalid data found for court: '{court_name}'. Data: {court_data}"
        )


class FetchWebpageError(Exception):
    """Custom exception for errors during webpage fetching."""

    pass


class InvalidTableHeadersError(ValueError):
    """Custom exception raised when table headers do not match the expected format."""

    pass
