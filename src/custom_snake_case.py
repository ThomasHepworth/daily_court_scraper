from functools import cached_property
from typing import ClassVar

from dlt.common.normalizers.naming.snake_case import (
    NamingConvention as SnakeCaseNamingConvention,
)


# TODO(ThomasHepworth): This is a hacky fix, where we search for predefined
# metadata columns and add a double underscore. Improve if given time.
class NamingConvention(SnakeCaseNamingConvention):
    _METADATA_COLUMNS: ClassVar[set[str]] = {"valid_from", "valid_to"}

    @cached_property
    def _metadata_columns(self) -> set[str]:
        """
        Expands metadata columns to include all possible prefixes and caches the result.
        """
        prefixes = ["", "_", "__"]
        return {
            f"{prefix}{column}"
            for column in self._METADATA_COLUMNS
            for prefix in prefixes
        }

    def normalize_identifier(self, identifier: str) -> str:
        normalized_identifier = super().normalize_identifier(identifier)

        if normalized_identifier in self._metadata_columns:
            return f"__{normalized_identifier.lstrip('_')}"

        return normalized_identifier
