from abc import abstractmethod
from typing import Optional

from .data_source import DataSource
from ..utils import Connectable, DBConfig
import polars as pl


class DataBaseSource(DataSource, Connectable):
    """
    Abstract class for database sources.

    Methods:
        connect: Connect to the database.
        disconnect: Disconnect from the database.
        load_data: Load data from the database using a query.
        get_columns: Get the columns of a specific table in the database.
        initialize_pool: Initialize a connection pool.
        build_connection_string: Build a connection string.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
    ):
        if not connection_string and not db_config:
            raise ValueError("A connection string or DBConfig must be provided.")

        if connection_string:
            super().__init__(connection_string)

        self.db_config = db_config
        self.connected = False
        self._connection_pool = None

    @property
    def connected(self) -> bool:
        return self._connected

    @connected.setter
    def connected(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("The connected attribute must be a boolean.")
        self._connected = value

    @abstractmethod
    def connect(self) -> None:
        """Method to be overridden by subclasses for connecting to the database."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Method to be overridden by subclasses for disconnecting from the database."""
        pass

    @abstractmethod
    def load_data(self, query: str) -> pl.DataFrame:
        """Method to be overridden by subclasses to load data using a query."""
        pass

    @abstractmethod
    def get_columns(self, table_name: str) -> list[str]:
        """Method to be overridden by subclasses to get columns from a specific table."""
        pass

    @abstractmethod
    def initialize_pool(self, min_connections: int, max_connections: int) -> None:
        """Method to be overridden by subclasses to initialize the connection pool."""
        pass
