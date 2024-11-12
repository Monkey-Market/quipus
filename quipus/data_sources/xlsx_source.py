# pylint: disable=unreachable

from pathlib import Path
from typing import Any, Optional, Union, override

import polars as pl

from .file_source import FileSource


class XLSXSource(FileSource):
    """
    A class for loading and processing data from Excel (.xlsx) files.

    Inherits from:
        FileSource: Base class for handling file sources.

    Attributes:
        file_path (Union[str, Path]): Path to the Excel file.
        sheet (Optional[Union[str, int]]): The sheet name or index to be read.
        has_header (bool): Indicates if the Excel sheet has a header row.
        columns (Optional[list[str]]): Specific columns to read from the Excel sheet.
        read_options (Optional[dict[str, Any]]): Additional options for reading the file.
        date_columns (Optional[list[str]]): Columns that should be parsed as dates.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        sheet: Optional[Union[str, int]] = 0,
        has_header: bool = True,
        columns: Optional[list[str]] = None,
        read_options: Optional[dict[str, Any]] = None,
        date_columns: Optional[list[str]] = None,
    ):
        """
        Initializes an XLSXSource object with specified parameters.

        Parameters:
            file_path (Union[str, Path]): The path to the Excel file.
            sheet (Optional[Union[str, int]]): The sheet to read. Can be a sheet name or index.
                Defaults to the first sheet (0).
            has_header (bool): Specifies if the sheet has a header row. Defaults to True.
            columns (Optional[list[str]]): Columns to be read from the sheet. Defaults to None.
            read_options (Optional[dict[str, Any]]): Additional options for reading the file.
                Defaults to None.
            date_columns (list[str]): Columns to parse as dates. Defaults to None.
        """
        super().__init__(
            file_path=file_path,
            has_header=has_header,
            columns=columns,
            read_options=read_options,
            date_columns=date_columns,
        )
        self.sheet = sheet

    @property
    def sheet(self) -> Optional[Union[str, int]]:
        """
        Gets the sheet name or index.

        Returns:
            Optional[Union[str, int]]: The name or index of the sheet to be read.
        """
        return self._sheet

    @sheet.setter
    def sheet(self, value: Optional[Union[str, int]]) -> None:
        """
        Sets the sheet name or index.

        Parameters:
            value (Optional[Union[str, int]]): The sheet name (str) or index (int).

        Raises:
            TypeError: If the value is not a string or integer.
        """
        if not isinstance(value, (str, int)):
            raise TypeError("Sheet name must be a string or an integer.")
        self._sheet = value

    @override
    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the Excel file into a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the data from the specified sheet.
        """
        return pl.read_excel(
            source=self.file_path,
            sheet_name=self.sheet if isinstance(self.sheet, str) else None,
            sheet_id=self.sheet if isinstance(self.sheet, int) else None,
            has_header=self.has_header,
            columns=self.columns,
            **self.read_options,
        )

    def _select_sheet(
        self, result: Union[pl.DataFrame, dict[str, pl.DataFrame]]
    ) -> pl.DataFrame:
        """
        Selects the specified sheet from the result based on sheet_name or sheet_id.

        Parameters:
            result (Union[pl.DataFrame, dict[str, pl.DataFrame]]): The result from pl.read_excel,
            which can be a single DataFrame or a dictionary of DataFrames.

        Returns:
            pl.DataFrame: The DataFrame corresponding to the specified sheet.

        Raises:
            ValueError: If the sheet name or index is invalid.
        """
        if not isinstance(result, dict):
            return result

        sheet_names = list(result.keys())

        # Excel sheet passed as a string
        if isinstance(self.sheet, str):
            try:
                return result[self.sheet]
            except KeyError as e:
                raise ValueError(
                    f"Sheet name '{self.sheet}' not found in the Excel file."
                ) from e

        # Excel sheet passed as an integer (0-based index)
        if isinstance(self.sheet, int):
            try:
                return result[sheet_names[self.sheet]]
            except IndexError as e:
                raise ValueError(f"sheet_id {self.sheet} is out of range.") from e

        # Excel sheet not specified, returning first
        return result[sheet_names[0]]

    @override
    def get_columns(self, *args, **kwargs) -> list[str]:
        """
        Retrieves the column names from the Excel file.

        Returns:
            list[str]: A list of column names from the specified sheet.
        """
        result: pl.DataFrame = pl.read_excel(
            source=self.file_path,
            sheet_name=self.sheet if isinstance(self.sheet, str) else None,
            sheet_id=self.sheet if isinstance(self.sheet, int) else None,
            has_header=self.has_header,
            engine="calamine",
            read_options={"n_rows": 0},
        )

        return self._select_sheet(result).columns
