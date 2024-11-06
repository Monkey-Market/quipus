from enum import Enum


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
        return [item.value for item in cls]