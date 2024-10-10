import pandas as pd
from typing import Optional, List


class XLSXDataSource:
    """
    XLSX DataSource class to manage data retrieval from Excel (.xlsx) files.

    Attributes:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to load from the Excel file.
        dataframe (Optional[pd.DataFrame]): Loaded data as a pandas DataFrame.
    """

    def __init__(self, file_path: str, sheet_name: str):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.dataframe: Optional[pd.DataFrame] = None
        self.__load_data()

    def __load_data(self) -> None:
        """
        Load data from the Excel file into a pandas DataFrame.
        """
        self.dataframe = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

    @property
    def file_path(self) -> str:
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        if not isinstance(file_path, str):
            raise TypeError("'file_path' must be a string.")
        if not file_path.strip():
            raise ValueError("'file_path' cannot be an empty string.")
        self.__file_path = file_path

    @property
    def sheet_name(self) -> str:
        return self.__sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name: str) -> None:
        if not isinstance(sheet_name, str):
            raise TypeError("'sheet_name' must be a string.")
        self.__sheet_name = sheet_name

    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch all data from the Excel sheet as a pandas DataFrame.

        Returns:
            pd.DataFrame: Data loaded from the Excel sheet.
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

    def filter_data(self, query: str) -> pd.DataFrame:
        """
        Filter the Excel data using a pandas query string.

        Args:
            query (str): Query string to filter the data.

        Returns:
            pd.DataFrame: Filtered data based on the query.

        Raises:
            RuntimeError: If no data is loaded.
            ValueError: If the query is invalid.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the Excel file.")

        return self.dataframe.query(query)

    def __str__(self) -> str:
        return (
            f"XLSXDataSource(file_path={self.file_path}, sheet_name={self.sheet_name})"
        )
