from pathlib import Path
from typing import Any, Optional, Union

import polars as pl

from .file_source import FileSource


class XLSXSource(FileSource):

    def __init__(
        self,
        file_path: Union[str, Path],
        sheet: Optional[Union[str, int]] = 0,
        has_header: bool = True,
        columns: Optional[list[str]] = None,
        read_options: Optional[dict[str, Any]] = None,
        date_columns: Optional[list[str]] = None,
    ):
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
        return self._sheet

    @sheet.setter
    def sheet(self, value: Optional[Union[str, int]]) -> None:
        if not isinstance(value, (str, int)):
            raise TypeError("Sheet name must be a string or an integer.")
        self._sheet = value

    def load_data(self) -> pl.DataFrame:
        """
        Loads data from an Excel file into a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame with the data from the Excel file.
        """
        try:
            return pl.read_excel(
                source=self.file_path,
                sheet_name=self.sheet if isinstance(self.sheet, str) else None,
                sheet_id=self.sheet if isinstance(self.sheet, int) else None,
                has_header=self.has_header,
                columns=self.columns,
                **self.read_options,
            )
        except Exception as e:
            raise RuntimeError(
                f"An error ocurred while loading data from {self.file_path}."
            ) from e

    def _select_sheet(
        self, result: Union[pl.DataFrame, dict[str, pl.DataFrame]]
    ) -> pl.DataFrame:
        """
        Selects the correct sheet from the result based on sheet_name or sheet_id.

        Args:
            result (Union[pl.DataFrame, dict[str, pl.DataFrame]]): The result from pl.read_excel.

        Returns:
            pl.DataFrame: The selected DataFrame for the specified sheet.
        """
        if not isinstance(result, dict):
            return result

        sheet_names = list(result.keys())

        # Excel sheet passed as a string
        if isinstance(self.sheet, str):
            try:
                return result[self.sheet]
            except KeyError:
                raise ValueError(
                    f"Sheet name '{self.sheet}' not found in the Excel file."
                )

        # Excel sheet passed as an integer (0-based index)
        if isinstance(self.sheet, int):
            try:
                return result[sheet_names[self.sheet]]
            except IndexError:
                raise ValueError(f"sheet_id {self.sheet} is out of range.")

        # Excel sheet not specified, returning first
        return result[sheet_names[0]]

    def get_columns(self) -> list[str]:
        """
        Retrieves the list of columns from the Excel file.

        Returns:
            list[str]: A list of column names from the Excel file.
        """
        try:
            result = pl.read_excel(
                source=self.file_path,
                sheet_name=self.sheet if isinstance(self.sheet, str) else None,
                sheet_id=self.sheet if isinstance(self.sheet, int) else None,
                has_header=self.has_header,
                engine="calamine",
                read_options={"n_rows": 0},
            )

            df = self._select_sheet(result)

            return df.columns
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while getting columns from {self.file_path}."
            ) from e
