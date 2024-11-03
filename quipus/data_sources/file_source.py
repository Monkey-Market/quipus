from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional, Union
from .data_source import DataSource
from ..utils import EncodingType

import polars as pl


class FileSource(DataSource):
    """
    Abstract class for file data sources.

    Attributes:
        file_path: The path to the file.
        encoding: The encoding of the file.
        has_header: A boolean indicating if the file has a header.
        columns: A list of column names.
        read_options: Additional options for reading the file.
        date_columns: A list of column names that contain dates.

    Methods:
        load_data: Load the data from the file.
        get_columns: Get the columns of the file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        encoding: Optional[EncodingType] = "utf-8",
        has_header: bool = True,
        columns: Optional[list[str]] = None,
        read_options: Optional[dict[str, Any]] = None,
        date_columns: Optional[list[str]] = None,
    ):
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.has_header = has_header
        self.columns = columns
        self.read_options = read_options if read_options else {}
        self.date_columns = date_columns

    @property
    def file_path(self) -> Path:
        return self._file_path

    @file_path.setter
    def file_path(self, value: Union[str, Path]) -> None:
        if not Path(value).is_file():
            raise ValueError(
                f"Invalid file path: {value}. The path must point to an existing file."
            )
        self._file_path = Path(value)

    @property
    def encoding(self) -> EncodingType:
        return self._encoding

    @encoding.setter
    def encoding(self, value: Union[str, EncodingType]) -> None:
        if isinstance(value, str):
            if value not in EncodingType.values():
                raise ValueError(
                    f"Unsupported encoding: {value}. Must be one of {EncodingType.values()}."
                )
            value = EncodingType(value)
        elif not isinstance(value, EncodingType):
            raise ValueError(
                f"Unsupported type: {type(value)}. Expected EncodingType or str."
            )
        self._encoding = value

    @property
    def has_header(self) -> bool:
        return self._has_header

    @has_header.setter
    def has_header(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("has_header must be a boolean value.")
        self._has_header = value

    @property
    def columns(self) -> Optional[list[str]]:
        return self._columns

    @columns.setter
    def columns(self, value: Optional[list[str]]) -> None:
        if value is not None and not all(isinstance(col, str) for col in value):
            raise TypeError("All column names must be strings.")
        self._columns = value

    @property
    def read_options(self) -> dict[str, Any]:
        return self._read_options

    @read_options.setter
    def read_options(self, value: dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("read_options must be a dictionary.")
        self._read_options = value

    @property
    def date_columns(self) -> Optional[list[str]]:
        return self._date_columns

    @date_columns.setter
    def date_columns(self, value: Optional[list[str]]) -> None:
        if value is not None and not all(isinstance(col, str) for col in value):
            raise TypeError("All date column names must be strings.")
        self._date_columns = value

    @abstractmethod
    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the file into a Polars DataFrame.
        """
        pass

    @abstractmethod
    def get_columns(self) -> list[str]:
        """
        Get the list of column names from the data source.

        Returns:
            list[str]: list of column names.
        """
        pass
