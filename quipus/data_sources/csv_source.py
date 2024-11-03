from pathlib import Path
from typing import Optional, Union
import polars as pl

from .file_source import FileSource

from ..utils import EncodingType


class CSVSource(FileSource):

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
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        if len(value) != 1:
            raise ValueError("Delimiter must be a single character.")
        if not isinstance(value, str):
            raise TypeError("Delimiter must be a string.")
        self._delimiter = value

    @property
    def quote_char(self) -> Optional[str]:
        return self._quote_char

    @quote_char.setter
    def quote_char(self, value: Optional[str]) -> None:
        if value is not None and len(value) != 1:
            raise ValueError("Quote character must be a single character.")
        if value == self._delimiter:
            raise ValueError("Quote character cannot be the same as the delimiter.")
        if not isinstance(value, str):
            raise TypeError("Quote character must be a string.")
        self._quote_char = value

    @property
    def skip_rows(self) -> int:
        return self._skip_rows

    @skip_rows.setter
    def skip_rows(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("skip_rows must be an integer value.")
        if value < 0:
            raise ValueError("skip_rows must be a non-negative integer.")
        self._skip_rows = value

    @property
    def na_values(self) -> list[str]:
        return self._na_values

    @na_values.setter
    def na_values(self, value: list[str]) -> None:
        if not all(isinstance(v, str) for v in value):
            raise TypeError("na_values must be a list of strings.")
        self._na_values = value

    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the CSV file into a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame with the data from the CSV file.
        """
        try:
            return pl.read_csv(
                source=self.file_path,
                separator=self.delimiter,
                quote_char=self.quote_char,
                encoding=self.encoding,
                has_header=self.has_header,
                columns=self.columns,
                skip_rows=self.skip_rows,
                null_values=self.na_values,
            )
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while loading data from {self.file_path}."
            ) from e

    def get_columns(self) -> list[str]:
        """
        Retrieves the list of columns from the CSV file.

        Returns:
            list[str]: A list of column names.
        """
        try:
            df = pl.read_csv(
                source=self.file_path,
                n_rows=0,
                separator=self.delimiter,
                quote_char=self.quote_char,
                encoding=self.encoding,
                has_header=self.has_header,
            )
            return df.columns
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while reading column names from {self.file_path}."
            ) from e
