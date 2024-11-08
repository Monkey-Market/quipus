from pathlib import Path
from typing import Any, Optional, Union

from quipus.utils import EncodingType

from .data_source import DataSource


class FileSource(DataSource):
    """
    An abstract base class for file-based data sources.

    Attributes:
        file_path (Path): The path to the file.
        encoding (EncodingType): The encoding used for reading the file.
        has_header (bool): Indicates whether the file has a header row.
        columns (Optional[list[str]]): A list of column names to read from the file.
        read_options (dict[str, Any]): Additional options for reading the file.
        date_columns (Optional[list[str]]): A list of column names that contain date values.
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
        """
        Initializes a FileSource instance.

        Parameters:
            file_path (Union[str, Path]): The path to the file.
            encoding (Optional[EncodingType]): The encoding used for reading the file.
                Defaults to "utf-8".
            has_header (bool): Indicates if the file has a header row. Defaults to True.
            columns (Optional[list[str]]): List of specific columns to read. Defaults to None.
            read_options (Optional[dict[str, Any]]): Additional options for reading the file.
                Defaults to an empty dictionary.
            date_columns (Optional[list[str]]): List of columns containing date values.
                Defaults to None.
        """
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.has_header = has_header
        self.columns = columns
        self.read_options = read_options if read_options else {}
        self.date_columns = date_columns

    @property
    def file_path(self) -> Path:
        """
        Path: The path to the file.

        Raises:
            ValueError: If the provided file path does not point to an existing file.
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value: Union[str, Path]) -> None:
        """
        Sets the file path.

        Parameters:
            value (Union[str, Path]): The path to the file.

        Raises:
            ValueError: If the file path does not point to an existing file.
        """
        path = Path(value)
        if not path.is_file():
            raise ValueError(
                f"Invalid file path: {value}. The path must point to an existing file."
            )
        self._file_path = path

    @property
    def encoding(self) -> EncodingType:
        """
        EncodingType: The encoding used for reading the file.

        Raises:
            ValueError: If the provided encoding is not supported.
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value: Union[str, EncodingType]) -> None:
        """
        Sets the file encoding.

        Parameters:
            value (Union[str, EncodingType]): The encoding type.

        Raises:
            ValueError: If the encoding is not supported.
            TypeError: If the type is incorrect.
        """
        if isinstance(value, str):
            if value not in EncodingType:
                raise ValueError(
                    f"Unsupported encoding: {value}. Must be one of {EncodingType.values()}."
                )
            value = EncodingType(value)

        if not isinstance(value, EncodingType):
            raise TypeError(
                "Unsupported type for encoding. Expected EncodingType or str."
            )

        self._encoding = value

    @property
    def has_header(self) -> bool:
        """
        bool: Indicates if the file has a header row.

        Raises:
            TypeError: If the value is not a boolean.
        """
        return self._has_header

    @has_header.setter
    def has_header(self, value: bool) -> None:
        """
        Sets whether the file has a header row.

        Parameters:
            value (bool): Boolean indicating if the file has a header.

        Raises:
            TypeError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("has_header must be a boolean value.")
        self._has_header = value

    @property
    def columns(self) -> Optional[list[str]]:
        """
        Optional[list[str]]: A list of column names to read.

        Raises:
            TypeError: If any column name is not a string.
        """
        return self._columns

    @columns.setter
    def columns(self, value: Optional[list[str]]) -> None:
        """
        Sets the columns to read from the file.

        Parameters:
            value (Optional[list[str]]): List of column names.

        Raises:
            ValueError: If columns is empty.
            TypeError: If any column name is not a string or columns is not a list.
        """
        if value is None:
            self._columns = value
            return

        if not isinstance(value, list):
            raise TypeError("columns must be a list of column names.")

        if not value:
            raise ValueError("columns cannot be empty.")

        if not all(isinstance(col, str) for col in value):
            raise TypeError("All column names must be strings.")

        self._columns = value

    @property
    def read_options(self) -> dict[str, Any]:
        """
        dict[str, Any]: Additional options for reading the file.

        Raises:
            TypeError: If read_options is not a dictionary.
        """
        return self._read_options

    @read_options.setter
    def read_options(self, value: dict[str, Any]) -> None:
        """
        Sets additional options for reading the file.

        Parameters:
            value (dict[str, Any]): A dictionary of read options.

        Raises:
            TypeError: If read_options is not a dictionary.
        """
        if not isinstance(value, dict):
            raise TypeError("read_options must be a dictionary.")
        self._read_options = value

    @property
    def date_columns(self) -> Optional[list[str]]:
        """
        Optional[list[str]]: A list of column names containing date values.

        Raises:
            TypeError: If any date column name is not a string.
        """
        return self._date_columns

    @date_columns.setter
    def date_columns(self, value: Optional[list[str]]) -> None:
        """
        Sets the columns containing date values.

        Parameters:
            value (Optional[list[str]]): List of column names containing dates.

        Raises:
            TypeError: If any date column name is not a string or date_columns is not a list.
            ValueError: If date_columns is empty.
        """
        if value is None:
            self._date_columns = value
            return

        if not isinstance(value, list):
            raise TypeError("date_columns must be a list of column names.")

        if not value:
            raise ValueError("date_columns cannot be empty.")

        if not all(isinstance(col, str) for col in value):
            raise TypeError("All date column names must be strings.")

        self._date_columns = value
