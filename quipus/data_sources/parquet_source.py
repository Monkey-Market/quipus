from pathlib import Path
from typing import Any, Optional, Union, override

import polars as pl

from .file_source import FileSource


class ParquetSource(FileSource):
    """
    A class for loading and processing data from Parquet files.

    Inherits from:
        FileSource: Base class for handling file sources.

    Attributes:
        file_path (Union[str, Path]): The path to the Parquet file.
        columns (Optional[list[str]]): Specific columns to read from the file.
        read_options (Optional[dict[str, Any]]): Additional options for reading the file.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        columns: Optional[list[str]] = None,
        read_options: Optional[dict[str, Any]] = None,
    ):
        """
        Initializes a ParquetSource instance with the specified parameters.

        Parameters:
            file_path (Union[str, Path]): The path to the Parquet file.
            columns (Optional[list[str]]): Columns to be read from the file.
                Defaults to None, which reads all columns.
            read_options (Optional[dict[str, Any]]): Additional options for reading
                the file, passed directly to the Polars reader. Defaults to None.
        """
        super().__init__(
            file_path=file_path,
            columns=columns,
            read_options=read_options,
        )

    @override
    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the Parquet file into a Polars DataFrame.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the data from the Parquet file.

        Raises:
            RuntimeError: If an error occurs while loading the data.
        """
        return pl.read_parquet(
            source=self.file_path, columns=self.columns, **self.read_options
        )

    @override
    def get_columns(self, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of columns from the Parquet file.

        Returns:
            list[str]: A list of column names from the Parquet file.
        """
        df = pl.read_parquet(
            source=self.file_path,
            n_rows=0,
            **self.read_options,
        )
        return df.columns
