from typing import Optional
from mysql.connector import pooling, connect, Error

from ..utils import DBConfig
from .database_source import DataBaseSource

import polars as pl


class MySQLSource(DataBaseSource):
    """
    Class for managing connections to a MySQL database using Oracle's mysql-connector-python and connection pooling.

    Attributes:
        connection_string (str): The connection string for the MySQL database.
        query: The query to execute on the database.
    """

    def __init__(
        self,
        query: str,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
    ):
        if db_config and not connection_string:
            connection_string = (
                f"mysql://{db_config.user}:{db_config.password}@"
                f"{db_config.host}:{db_config.port}/{db_config.database}"
            )
        super().__init__(connection_string, db_config)
        self._connection_pool = None
        self.query = query

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The query must be a string.")
        if value.strip() == "":
            raise ValueError("The query cannot be empty.")
        self._query = value

    def initialize_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Initializes the connection pool for MySQL.

        Args:
            min_connections (int): The minimum number of connections in the pool.
            max_connections (int): The maximum number of connections in the pool.
        """
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=max_connections,
                pool_reset_session=True,
                user=self.db_config.user,
                password=self.db_config.password,
                host=self.db_config.host,
                port=self.db_config.port,
                database=self.db_config.database,
            )
        except Error as e:
            raise RuntimeError(f"Error initializing connection pool: {e}")

    def connect(self) -> None:
        """Obtains a connection from the pool and sets the connected status to True."""
        if not self._connection_pool:
            raise RuntimeError("Connection pool is not initialized.")
        try:
            self._connection = self._connection_pool.get_connection()
            self.connected = True
        except Error as e:
            raise RuntimeError(f"Error connecting to the database: {e}")

    def disconnect(self):
        """Disconnects from the database and sets the connected status to False."""
        if self._connection and self._connection:
            try:
                self._connection.close()
                self.connected = False
            except Error as e:
                raise RuntimeError(f"Error disconnecting from the database: {e}")
        else:
            raise RuntimeError("No active connection to disconnect.")

    def load_data(self) -> pl.DataFrame:
        """
        Executes a query to load data from the MySQL database.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the data from the query.
        """
        if not self._connected or not self._connection:
            raise RuntimeError("Not connected to the MySQL database.")

        if not self.query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed for loading data.")

        try:
            cursor = self._connection.cursor()
            cursor.execute(self.query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return self.to_polars_df(result, columns)
        except Error as e:
            raise RuntimeError(f"Error executing query: {e}")

    def get_columns(self, table_name: str) -> list[str]:
        """
        Retrieves the list of columns from a specific table in the MySQL database.

        Args:
            table_name (str): The name of the table.

        Returns:
            list[str]: A list of column names.
        """

        if not self._connected or not self._connection:
            raise RuntimeError("Not connected to the MySQL database.")

        query = f"SHOW COLUMNS FROM {table_name}"
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            columns = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return columns
        except Error as e:
            raise RuntimeError(f"Error retrieving columns: {e}")
