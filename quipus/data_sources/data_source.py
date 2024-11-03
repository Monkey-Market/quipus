from abc import ABC, abstractmethod
from typing import List, Tuple, Union
import polars as pl


class DataSource(ABC):
    """
    Abstract class for data sources.

    Methods:
        load_data: Load the data from the data source.
        get_columns: Get the columns of the data source.
    """

    @abstractmethod
    def load_data(self) -> pl.DataFrame:
        """Method to be overridden by subclasses to load data from the data source."""
        pass

    @abstractmethod
    def get_columns(self) -> List[str]:
        """Method to be overridden by subclasses to get all columns from the data source."""
        pass

    def to_polars_df(
        self, data: Union[pl.DataFrame, List[Tuple]], columns: List[str] = None
    ) -> pl.DataFrame:
        """
        Converts data to a Polars DataFrame.

        Args:
            data (Union[pl.DataFrame, List[tuple]]): The data to convert.
            columns (List[str], optional): The column names for the DataFrame.

        Returns:
            pl.DataFrame: The converted Polars DataFrame.
        """
        if isinstance(data, pl.DataFrame):
            return data
        elif isinstance(data, list) and all(isinstance(row, Tuple) for row in data):
            return pl.DataFrame(data, schema=columns, orient="row")
        else:
            raise ValueError(
                "Unsupported data format for conversion to Polars DataFrame."
            )
