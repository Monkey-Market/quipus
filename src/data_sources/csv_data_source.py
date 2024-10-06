import pandas as pd
from typing import Optional, List, Any


class CSVDataSource:
    """
    CSV DataSource class to manage data retrieval from CSV files.

    Attributes:
        file_path (str): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file.
        encoding (str): Encoding of the CSV file.
        dataframe (Optional[pd.DataFrame]): Loaded data as a pandas DataFrame.
    """

    def __init__(self, file_path: str, delimiter: str = ",", encoding: str = "utf-8"):
        self.__file_path = file_path
        self.__delimiter = delimiter
        self.__encoding = encoding
        self.__dataframe: Optional[pd.DataFrame] = None
        self.__load_data()

    def __load_data(self) -> None:
        """
        Load data from the CSV file into a pandas DataFrame.
        """
        try:
            self.__dataframe = pd.read_csv(
                self.file_path, delimiter=self.delimiter, encoding=self.encoding
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load CSV data: {e}")

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
        self.__load_data()

    @property
    def delimiter(self) -> str:
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter: str) -> None:
        if not isinstance(delimiter, str):
            raise TypeError("'delimiter' must be a string.")
        self.__delimiter = delimiter
        self.__load_data()

    @property
    def encoding(self) -> str:
        return self.__encoding

    @encoding.setter
    def encoding(self, encoding: str) -> None:
        if not isinstance(encoding, str):
            raise TypeError("'encoding' must be a string.")
        self.__encoding = encoding
        self.__load_data()

    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch all data from the CSV file as a pandas DataFrame.

        Returns:
            pd.DataFrame: Data loaded from the CSV file.
        """
        if self.__dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")
        return self.__dataframe

    def get_columns(self) -> List[str]:
        """
        Get the list of column names from the CSV data.

        Returns:
            List[str]: Column names.
        """
        if self.__dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")
        return list(self.__dataframe.columns)

    def filter_data(self, query: str) -> pd.DataFrame:
        """
        Filter the CSV data using a pandas query string.

        Args:
            query (str): Query string to filter the data.

        Returns:
            pd.DataFrame: Filtered data based on the query.

        Raises:
            RuntimeError: If no data is loaded.
            ValueError: If the query is invalid.
        """
        if self.__dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")
        try:
            return self.__dataframe.query(query)
        except Exception as e:
            raise ValueError(f"Failed to filter data: {e}")

    def __str__(self) -> str:
        return f"CSVDataSource(file_path={self.file_path}, delimiter={self.delimiter}, encoding={self.encoding})"
