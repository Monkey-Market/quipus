from abc import ABC, abstractmethod
from typing import Union

import polars as pl


class DataSource(ABC):
    """
    An abstract base class for data sources.
    """

    @abstractmethod
    def load_data(self) -> pl.DataFrame:
        """
        Abstract method to be overridden by subclasses to load data from the data source.

        Returns:
            pl.DataFrame: The loaded data as a Polars DataFrame.
        """

    @abstractmethod
    def get_columns(self, *args, **kwargs) -> list[str]:
        """
        Abstract method to be overridden by subclasses to retrieve column names from a data source.

        Returns:
            list[str]: A list of column names.
        """

    def to_polars_df(
        self,
        data: Union[pl.DataFrame, list[tuple], list[dict]],
        columns: list[str] = None,
    ) -> pl.DataFrame:
        """
        Converts the provided data into a Polars DataFrame.

        Parameters:
            data (Union[pl.DataFrame, list[tuple], list[dict]]): The data to be converted.
              Can be a Polars DataFrame, a list of tuples, or a list of dictionaries.
            columns (list[str]): The column names for the DataFrame when data is
              a list of tuples. Defaults to None.

        Returns:
            pl.DataFrame: The converted Polars DataFrame.

        Raises:
            TypeError: If the provided data is not in an acceptable format.
            ValueError: If the data format is unsupported for conversion.
        """
        if isinstance(data, pl.DataFrame):
            return data

        if not isinstance(data, list):
            raise TypeError(
                "Data must be a Polars DataFrame, a list of tuples, or a list of dictionaries."
            )

        if all(isinstance(row, tuple) for row in data):
            if columns is None:
                raise ValueError(
                    "Columns must be provided when data is a list of tuples."
                )
            return pl.DataFrame(data, schema=columns, orient="row")

        if all(isinstance(row, dict) for row in data):
            return pl.DataFrame(data)

        raise TypeError(
            "All elements in the data list must be either tuples or dictionaries."
        )
