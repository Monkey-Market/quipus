from abc import abstractmethod
from .data_source import DataSource
from ..utils import Connectable
from typing import List

import polars as pl


class DataBaseSource(DataSource, Connectable):
    """
    Abstract class for database sources.

    Attributes:
        connection_string: The connection string for the database.
        connected: A boolean indicating if the database is connected.

    Methods:
        connect: Connect to the database.
        disconnect: Disconnect from the database.
        load_data: Load data from the database using a query.
        get_columns: Get the columns of a specific table in the database.
        initialize_pool: Initialize a connection pool.
    """

    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._connected = False
        self._connection_pool = None

    @property
    def connection_string(self) -> str:
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The connection string must be a string.")

        if value.strip() == "":
            raise ValueError("The connection string cannot be empty.")
        self._connection_string = value

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
    def get_columns(self, table_name: str) -> List[str]:
        """Method to be overridden by subclasses to get columns from a specific table."""
        pass

    @abstractmethod
    def initialize_pool(self, min_connections: int, max_connections: int) -> None:
        """Method to be overridden by subclasses to initialize the connection pool."""
        pass
