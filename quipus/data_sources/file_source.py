from abc import abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import polars as pl
from .data_source import DataSource
from ..utils import EncodingType, VALID_ENCODINGS


class FileSource(DataSource):
    def __init__(
        self,
        file_path: Union[str, Path],
        encoding: Optional[EncodingType] = "utf-8",
        has_header: bool = True,
        columns: Optional[List[str]] = None,
        read_options: Optional[Dict[str, Any]] = None,
        date_columns: Optional[List[str]] = None,
    ):
        self._file_path = Path(file_path)
        self._encoding = encoding
        self._has_header = has_header
        self._columns = columns
        self._read_options = read_options if read_options else {}
        self._date_columns = date_columns

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
    def encoding(self, value: EncodingType) -> None:
        if value not in VALID_ENCODINGS:
            raise ValueError(
                f"Unsupported encoding: {value}. Must be one of {VALID_ENCODINGS}."
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
    def columns(self) -> Optional[List[str]]:
        return self._columns

    @columns.setter
    def columns(self, value: Optional[List[str]]) -> None:
        if value is not None and not all(isinstance(col, str) for col in value):
            raise TypeError("All column names must be strings.")
        self._columns = value

    @property
    def read_options(self) -> Dict[str, Any]:
        return self._read_options

    @read_options.setter
    def read_options(self, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("read_options must be a dictionary.")
        self._read_options = value

    @property
    def date_columns(self) -> Optional[List[str]]:
        return self._date_columns

    @date_columns.setter
    def date_columns(self, value: Optional[List[str]]) -> None:
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
    def get_columns(self) -> List[str]:
        """
        Get the list of column names from the data source.

        Returns:
            List[str]: List of column names.
        """
        pass
