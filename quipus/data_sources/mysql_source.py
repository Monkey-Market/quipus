from typing import Optional, override
from mysql.connector import pooling, Error

from quipus.utils import DBConfig
from quipus.data_sources import DataBaseSource

import polars as pl


class MySQLSource(DataBaseSource):
    """
    A class for managing connections and data retrieval from a MySQL database using
    Oracle's `mysql-connector-python` with connection pooling.

    Attributes:
        query (str): The SQL query to be executed on the database.

    Methods:
        initialize_pool(min_connections: int, max_connections: int) -> None:
            Initializes the connection pool for the MySQL database.

        connect() -> None:
            Establishes a connection from the pool and marks the connection as active.

        disconnect() -> None:
            Closes the active connection and sets the connection status to inactive.

        load_data() -> pl.DataFrame:
            Executes the configured SQL query and loads the data into a Polars DataFrame.

        get_columns(table_name: str) -> list[str]:
            Retrieves column names from a specific table in the MySQL database.
    """

    def __init__(
        self,
        query: str,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
    ):
        """
        Initializes a MySQLSource instance with a query and optional connection details.

        Parameters:
            query (str): The SQL query to execute.
            connection_string (Optional[str], optional): The connection string for the database.
                Defaults to None, which constructs it from db_config if provided.
            db_config (Optional[DBConfig], optional): A DBConfig instance for constructing
                the connection string. Defaults to None.

        Raises:
            ValueError: If the query is not a valid string.
        """
        if db_config and not connection_string:
            connection_string = (
                f"mysql://{db_config.user}:{db_config.password}@"
                f"{db_config.host}:{db_config.port}/{db_config.database}"
            )
        super().__init__(connection_string, db_config)
        self._connection = None
        self.query = query

    @property
    def query(self) -> str:
        """
        str: The SQL query to be executed on the database.

        Raises:
            ValueError: If the query is not a string or is empty.
        """
        return self._query

    @query.setter
    def query(self, value: str) -> None:
        """
        Sets the SQL query to be executed.

        Parameters:
            value (str): The SQL query.

        Raises:
            ValueError: If the query is not a string or is empty.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The query must be a non-empty string.")
        self._query = value

    def initialize_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Initializes the connection pool for MySQL.

        Parameters:
            min_connections (int): The minimum number of connections in the pool. Defaults to 1.
            max_connections (int): The maximum number of connections in the pool. Defaults to 10.
        """
        self._connection_pool = pooling.MySQLConnectionPool(
            pool_size=max_connections,
            pool_reset_session=True,
            user=self.db_config.user,
            password=self.db_config.password,
            host=self.db_config.host,
            port=self.db_config.port,
            database=self.db_config.database,
        )

    def connect(self) -> None:
        """
        Obtains a connection from the connection pool and sets the connected status to True.

        Raises:
            RuntimeError: If an error occurs while trying to connect to the database.
        """
        if not hasattr(self, "_connection_pool") or self._connection_pool is None:
            self.initialize_pool()

        if not self._connection:
            try:
                self._connection = self._connection_pool.get_connection()
                self.connected = True
            except Error as e:
                raise ConnectionError(f"Error connecting to the database: {e}")

    def disconnect(self):
        """
        Closes the current connection and sets the connected status to False.

        Raises:
            ConnectionError: If there is no active connection or an error occurs during disconnection.
        """
        if not self._connection:
            raise ConnectionError("No active connection to disconnect.")

        try:
            self._connection.close()
            self.connected = False
        except Error as e:
            raise ConnectionError(f"Error disconnecting from the database: {e}")

    def load_data(self) -> pl.DataFrame:
        """
        Executes the configured SQL query and loads the data from the MySQL database
        into a Polars DataFrame.

        Returns:
            pl.DataFrame: A DataFrame containing the query result.

        Raises:
            ConnectionError: If not connected to the database.
            RuntimeError: If an error occurs during query execution.
        """
        if not self._connected or not self._connection:
            raise ConnectionError("Not connected to the MySQL database.")

        try:
            cursor = self._connection.cursor()
            cursor.execute(self.query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return self.to_polars_df(result, columns)
        except Error as e:
            raise RuntimeError(f"Error executing query: {e}")

    @override
    def get_columns(self, table_name: str, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of columns from a specified table in the MySQL database.

        Parameters:
            table_name (str): The name of the table to retrieve column names from.

        Returns:
            list[str]: A list of column names from the table.

        Raises:
            ConnectionError: If not connected to the database.
            RuntimeError: If an error occurs during retrieval.
        """
        if not self._connected or not self._connection:
            raise ConnectionError("Not connected to the MySQL database.")

        query = f"SHOW COLUMNS FROM {table_name}"
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            columns = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return columns
        except Error as e:
            raise RuntimeError(f"Error retrieving columns: {e}")