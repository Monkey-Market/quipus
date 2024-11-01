from pathlib import Path
from typing import Union, Optional, List

import polars as pl


class XLSXDataSource:
    """
    XLSX DataSource class to manage data retrieval from Excel (.xlsx) files.

    Attributes:
        file_path (Union[Path, str]): Path to the Excel file.
        sheet_name (str): Name of the sheet to load from the Excel file.
        dataframe (Optional[pl.DataFrame]): Loaded data as a polars DataFrame.
    """

    def __init__(self, file_path: Union[Path, str], sheet_name: str):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.dataframe: Optional[pl.DataFrame] = None
        self.__load_data()

    def __load_data(self) -> None:
        """
        Load data from the Excel file into a polars DataFrame.
        """
        self.dataframe = pl.read_excel(self.file_path, sheet_name=self.sheet_name)

    @property
    def file_path(self) -> Union[Path, str]:
        """
        Get the path to the Excel file.

        Returns:
            Union[Path, str]: Path to the Excel file.
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: Union[Path, str]) -> None:
        """
        Set the path to the Excel file.

        Args:
            file_path (str): Path to the Excel file.

        Raises:
            TypeError: If 'file_path' is not a string.
            ValueError: If 'file_path' is an empty string.
        """
        if not isinstance(file_path, (Path, str)):
            raise TypeError("'file_path' must be either a string or 'Path' object.")

        # Ensure if path exists
        path = Path(file_path) if isinstance(file_path, str) else file_path
        if not path.exists() or path.is_dir():
            raise FileNotFoundError(f"'{file_path}' does not exist.")
        self.__file_path = path

    @property
    def sheet_name(self) -> str:
        """
        Get the name of the sheet to load from the Excel file.

        Returns:
            str: Name of the sheet."""
        return self.__sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name: str) -> None:
        """
        Set the name of the sheet to load from the Excel file.

        Args:
            sheet_name (str): Name of the sheet.

        Raises:
            TypeError: If 'sheet_name' is not a string.
        """
        if not isinstance(sheet_name, str):
            raise TypeError("'sheet_name' must be a string.")
        self.__sheet_name = sheet_name

    def fetch_data(self) -> pl.DataFrame:
        """
        Fetch all data from the Excel sheet as a polars DataFrame.

        Returns:
            pl.DataFrame: Data loaded from the Excel sheet.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the Excel file.")
        return self.dataframe

    def get_columns(self) -> List[str]:
        """
        Get the list of column names from the Excel data.

        Returns:
            List[str]: Column names.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the Excel file.")
        return list(self.dataframe.columns)

    def filter_data(self, query: str) -> pl.DataFrame:
        """
        Filter the Excel data using a polars query string.

        Args:
            query (str): Query string to filter the data.

        Returns:
            pl.DataFrame: Filtered data based on the query.

        Raises:
            RuntimeError: If no data is loaded.
            ValueError: If the query is invalid.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the Excel file.")

        try:
            return self.dataframe.sql(query)
        except Exception:
            raise ValueError("Invalid query provided.")

    def __str__(self) -> str:
        """
        Get a string representation of the XLSXDataSource object.

        Returns:
            str: String representation of the object.
        """
        return (
            f"XLSXDataSource(file_path={self.file_path}, sheet_name={self.sheet_name})"
        )
