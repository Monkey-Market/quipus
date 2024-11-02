from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import polars as pl
from .file_source import FileSource


class ParquetSource(FileSource):
    def __init__(
        self,
        file_path: Union[str, Path],
        columns: Optional[List[str]] = None,
        read_options: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            file_path=file_path,
            columns=columns,
            read_options=read_options,
        )

    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the Parquet file into a Polars DataFrame.
        """
        try:
            df = pl.read_parquet(
                source=self.file_path, columns=self.columns, **self.read_options
            )
            return df
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while loading data from {self.file_path}."
            ) from e

    def get_columns(self) -> List[str]:
        """
        Retrieves the list of columns from the Parquet file.

        Returns:
            List[str]: A list of column names.
        """
        try:
            df = pl.read_parquet(
                source=self.file_path,
                n_rows=0,
                **self.read_options,
            )
            return df.columns
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while getting columns from {self.file_path}."
            ) from e
