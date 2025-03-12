from pathlib import Path
from typing import Union, Optional, List

import polars as pl


class CSVDataSource:
    """
    CSV DataSource class to manage data retrieval from CSV files.

    Attributes:
        file_path (Union[Path, str]): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file.
        encoding (str): Encoding of the CSV file.
        dataframe (Optional[pl.DataFrame]): Loaded data as a polars DataFrame.
    """

    def __init__(
        self, file_path: Union[Path, str], delimiter: str = ",", encoding: str = "utf8"
    ):
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding
        self.dataframe: Optional[pl.DataFrame] = None
        self.__load_data()

    def __load_data(self) -> None:
        """
        Load data from the CSV file into a polars DataFrame.
        """
        self.dataframe = pl.read_csv(
            source=self.file_path, separator=self.delimiter, encoding=self.encoding
        )

    @property
    def file_path(self) -> Union[Path, str]:
        """
        Get the path to the CSV file.

        Returns:
            Union[Path, str]: Path to the CSV file.
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: Union[Path, str]) -> None:
        """
        Set the path to the CSV file.

        Args:
            file_path (Union[Path, str]): Path to the CSV file.

        Raises:
            TypeError: If 'file_path' is not a string.
            ValueError: If 'file_path' is an empty string.
        """
        if not isinstance(file_path, (Path, str)):
            raise TypeError("'file_path' must be either a string or 'Path' object.")

        # Ensure that path exists
        file_path = Path(file_path) if isinstance(file_path, str) else file_path
        if not file_path.exists() or file_path.is_dir():
            raise FileNotFoundError(f"'{file_path}' does not exist.")
        self.__file_path = file_path

    @property
    def delimiter(self) -> str:
        """
        Get the delimiter used in the CSV file.

        Returns:
            str: Delimiter used in the CSV file.
        """
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter: str) -> None:
        """
        Set the delimiter used in the CSV file.

        Args:
            delimiter (str): Delimiter used in the CSV file.

        Raises:
            TypeError: If 'delimiter' is not a string.
        """
        if not isinstance(delimiter, str):
            raise TypeError("'delimiter' must be a string.")
        self.__delimiter = delimiter

    @property
    def encoding(self) -> str:
        """
        Get the encoding of the CSV file.

        Returns:
            str: Encoding of the CSV file.
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, encoding: str) -> None:
        if not isinstance(encoding, str):
            raise TypeError("'encoding' must be a string.")
        self.__encoding = encoding

    def fetch_data(self) -> pl.DataFrame:
        """
        Fetch all data from the CSV file as a polars DataFrame.

        Returns:
            pl.DataFrame: Data loaded from the CSV file.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")
        return self.dataframe

    def get_columns(self) -> List[str]:
        """
        Get the list of column names from the CSV data.

        Returns:
            List[str]: Column names.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")
        return list(self.dataframe.columns)

    def filter_data(self, query: str) -> pl.DataFrame:
        """
        Filter the CSV data using a polars query string.

        Args:
            query (str): Query string to filter the data.

        Returns:
            pl.DataFrame: Filtered data based on the query.

        Raises:
            RuntimeError: If no data is loaded.
            ValueError: If the query is invalid.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded from the CSV file.")

        try:
            return self.dataframe.sql(query=query)
        except Exception as e:
            raise ValueError(f"Invalid query: {query}") from e

    def __str__(self) -> str:
        """
        Get a string representation of the CSVDataSource object.

        Returns:
            str: String representation of the object.
        """
        return (
            f"CSVDataSource(file_path={self.file_path}, "
            f"delimiter={self.delimiter}, encoding={self.encoding})"
        )
