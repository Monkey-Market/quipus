from pathlib import Path
from typing import Optional, Union, override

import polars as pl

from quipus.utils import EncodingType

from .file_source import FileSource


class CSVSource(FileSource):
    """
    A class for loading and processing data from CSV files.

    Attributes:
        file_path (Union[str, Path]): The path to the CSV file.
        delimiter (str): The character used to separate values in the CSV file.
        quote_char (Optional[str]): The character used to quote strings in the CSV file.
        skip_rows (int): The number of rows to skip at the start of the file.
        na_values (list[str]): A list of values to interpret as missing/NA.
        encoding (Optional[EncodingType]): The encoding used for reading the file.
        has_header (bool): Indicates if the CSV file has a header row.
        columns (Optional[list[str]]): A list of columns to read from the file.
        date_columns (Optional[list[str]]): A list of column names that contain date values.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        delimiter: str = ",",
        quote_char: Optional[str] = None,
        skip_rows: int = 0,
        na_values: Optional[list[str]] = None,
        encoding: Optional[EncodingType] = "utf-8",
        has_header: bool = True,
        columns: Optional[list[str]] = None,
        date_columns: Optional[list[str]] = None,
    ):
        """
        Initializes a CSVSource instance with the specified parameters.

        Parameters:
          file_path (Union[str, Path]): The path to the CSV file.
          delimiter (str): The character used to separate values. Defaults to ",".
          quote_char (Optional[str]): Character used to quote strings. Defaults to None.
          skip_rows (int): The number of rows to skip at the start of the file. Defaults to 0.
          na_values (Optional[list[str]]): A list of values to treat as missing. Defaults to None.
          encoding (Optional[EncodingType]): The file encoding. Defaults to "utf-8".
          has_header (bool): Indicates if the file has a header row. Defaults to True.
          columns (Optional[list[str]]): Columns to read from the file. Defaults to None.
          date_columns (Optional[list[str]]): Columns containing date values. Defaults to None.
        """
        super().__init__(
            file_path=file_path,
            encoding=encoding,
            has_header=has_header,
            columns=columns,
            date_columns=date_columns,
        )
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.skip_rows = skip_rows
        self.na_values = na_values if na_values else []

    @property
    def delimiter(self) -> str:
        """
        str: The character used to separate values in the CSV file.
        """
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        """
        Sets the delimiter used to separate values in the CSV file.

        Parameters:
            value (str): The delimiter character.

        Raises:
            ValueError: If the delimiter is not a single character.
            TypeError: If the delimiter is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Delimiter must be a string.")
        if len(value) != 1:
            raise ValueError("Delimiter must be a single character.")
        self._delimiter = value

    @property
    def quote_char(self) -> Optional[str]:
        """
        Optional[str]: The character used to quote strings in the CSV file.

        Raises:
            ValueError: If `quote_char` is the same as the delimiter or not a single character.
            TypeError: If `quote_char` is not a string.
        """
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value: Optional[str]) -> None:
        """
        Sets the quote character used to quote strings in the CSV file.

        Parameters:
            value (Optional[str]): The quote character.

        Raises:
            ValueError: If the `quote_char` is the same as the delimiter or not a single character.
            TypeError: If the `quote_char` is not a string.
        """
        if value is None:
            self._quote_char = value
            return
        if not isinstance(value, str):
            raise TypeError("Quote character must be a string.")
        if len(value) != 1:
            raise ValueError("Quote character must be a single character.")
        if value == self.delimiter:
            raise ValueError("Quote character cannot be the same as the delimiter.")
        self._quote_char = value

    @property
    def skip_rows(self) -> int:
        """
        int: The number of rows to skip at the start of the CSV file.

        Raises:
            TypeError: If skip_rows is not an integer.
            ValueError: If skip_rows is negative.
        """
        return self._skip_rows

    @skip_rows.setter
    def skip_rows(self, value: int) -> None:
        """
        Sets the number of rows to skip at the start of the CSV file.

        Parameters:
            value (int): The number of rows to skip.

        Raises:
            TypeError: If skip_rows is not an integer.
            ValueError: If skip_rows is negative.
        """
        if not isinstance(value, int):
            raise TypeError("skip_rows must be an integer value.")
        if value < 0:
            raise ValueError("skip_rows must be a non-negative integer.")
        self._skip_rows = value

    @property
    def na_values(self) -> list[str]:
        """
        list[str]: The values to treat as missing/NA.

        Raises:
            TypeError: If any value in na_values is not a string.
        """
        return self._na_values

    @na_values.setter
    def na_values(self, value: list[str]) -> None:
        """
        Sets the values to treat as missing/NA.

        Parameters:
            value (list[str]): A list of values to treat as missing.

        Raises:
            TypeError: If any value in na_values is not a string.
        """
        if not isinstance(value, list):
            raise TypeError("na_values must be a list of strings.")

        if not all(isinstance(v, str) for v in value):
            raise TypeError("All values in na_values must be strings.")

        self._na_values = value

    @override
    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the CSV file into a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame with the data from the CSV file.
        """
        return pl.read_csv(
            source=self.file_path,
            separator=self.delimiter,
            quote_char=self.quote_char,
            encoding=self.encoding.value,
            has_header=self.has_header,
            columns=self.columns,
            skip_rows=self.skip_rows,
            null_values=self.na_values,
        )

    @override
    def get_columns(self, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of columns from the CSV file.

        Returns:
            list[str]: A list of column names.
        """
        df = pl.read_csv(
            source=self.file_path,
            n_rows=0,
            separator=self.delimiter,
            quote_char=self.quote_char,
            encoding=self.encoding.value,
            has_header=self.has_header,
        )
        return df.columns
