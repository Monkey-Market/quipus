from abc import ABC, abstractmethod
from typing import Any, List
import polars as pl


class DataSource(ABC):
    """
    Abstract class for data sources.

    Methods:
        load_data: Load the data from the data source.
        get_columns: Get the columns of the data source.
        filter_data: Filter the data from the data source.
    """

    @abstractmethod
    def load_data(self) -> pl.DataFrame: ...

    @abstractmethod
    def get_columns(self) -> List[str]: ...
