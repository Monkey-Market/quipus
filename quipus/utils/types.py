from enum import Enum
from typing import TypedDict, Union

ValidReplacementValue = Union[str, int, float, None]


class ReplacementsDict(TypedDict, total=False):
    """
    TypedDict for template replacements validation.
    Allows dynamic string keys with values of type str, int, float or None.
    """

    key: ValidReplacementValue


class EncodingType(Enum):
    """
    Enum class for encoding types supported by the Quipus library.
    """

    UTF8 = "utf-8"
    ISO_8859_1 = "iso-8859-1"
    ASCII = "ascii"
    UTF16 = "utf-16"

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns a list of all the values in the EncodingType enum.

        Returns:
            list[str]: List of all the values in the EncodingType enum.
        """
        return [item.value for item in cls]
