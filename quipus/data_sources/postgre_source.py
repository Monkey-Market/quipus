from typing import Optional, override

import polars as pl
from psycopg_pool import ConnectionPool

from quipus.data_sources import DataBaseSource
from quipus.utils import DBConfig


class PostgreSQLSource(DataBaseSource):
    """
    A class for managing connections and data retrieval from a PostgreSQL database
    using psycopg v3 with connection pooling.

    Attributes:
        connection_string (str): The connection string for the PostgreSQL database.
        query (str): The SQL query to be executed on the database.

    Methods:
        initialize_pool(min_connections: int, max_connections: int) -> None:
            Initializes the connection pool for the database.

        connect() -> None:
            Obtains a connection from the pool and sets the connection status to active.

        disconnect() -> None:
            Releases the connection back to the pool and marks the status as disconnected.

        load_data() -> pl.DataFrame:
            Executes the provided SQL query and returns the result as a Polars DataFrame.

        get_columns(table_name: str) -> list[str]:
            Retrieves the column names for a specified table in the database.
    """

    def __init__(
        self,
        query: str,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
    ):
        """
        Initializes a PostgreSQLSource instance with a query and optional connection details.

        Parameters:
            query (str): The SQL query to execute.
            connection_string (Optional[str], optional): The connection string for the database.
                Defaults to None, which constructs it from db_config if provided.
            db_config (Optional[DBConfig], optional): A DBConfig instance for constructing
                the connection string. Defaults to None.
        """
        if db_config and not connection_string:
            connection_string = (
                f"postgresql://{db_config.user}:{db_config.password}@"
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
        if not isinstance(value, str):
            raise ValueError("The query must be a string.")
        if value.strip() == "":
            raise ValueError("The query cannot be empty.")
        self._query = value

    def initialize_pool(
        self, min_connections: int = 1, max_connections: int = 10
    ) -> None:
        """
        Initializes the connection pool for the PostgreSQL database.

        Parameters:
            min_connections (int): The minimum number of connections in the pool. Defaults to 1.
            max_connections (int): The maximum number of connections in the pool. Defaults to 10.
        """
        self._connection_pool = ConnectionPool(
            conninfo=self.connection_string,
            min_size=min_connections,
            max_size=max_connections,
        )

    def connect(self) -> None:
        """
        Obtains a connection from the connection pool and sets the connected status to True.

        Raises:
            RuntimeError: If an error occurs while trying to connect to the database.
        """
        if not hasattr(self, "_connection_pool") or self._connection_pool is None:
            self.initialize_pool()

        try:
            if not self._connection:
                self._connection = self._connection_pool.getconn()
                self._connection.autocommit = True
                self._connected = True
                print("Conexión exitosa.\n")

        except Exception as e:
            self._connected = False
            raise RuntimeError(f"Error connecting to the database: {e}") from e

    def disconnect(self) -> None:
        """
        Releases the current connection back to the pool and sets the connected status to False.

        Raises:
            RuntimeError: If an error occurs during disconnection or if no active connection exists.
        """
        if self._connected and self._connection:
            try:
                self._connection_pool.putconn(self._connection)
                self._connected = False
                print("\nDesconexión exitosa.")
            except Exception as e:
                raise RuntimeError(f"Error disconnecting from the database: {e}") from e
        else:
            raise RuntimeError("No active connection to disconnect.")

    def load_data(self) -> pl.DataFrame:
        """
        Executes the configured SQL query and loads data from the PostgreSQL database
        into a Polars DataFrame.

        Returns:
            pl.DataFrame: A DataFrame containing the query result.

        Raises:
            RuntimeError: If not connected to the database or if an error occurs during execution.
        """
        if not self._connected or not self._connection:
            raise RuntimeError("Not connected to the database.")

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(self.query)
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return self.to_polars_df(result, columns)
        except Exception as e:
            raise RuntimeError(f"Error loading data: {e}") from e

    @override
    def get_columns(self, table_name: str, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of column names from a specified table in the database.

        Parameters:
            table_name (str): The name of the table to retrieve column names from.

        Returns:
            list[str]: A list of column names from the table.

        Raises:
            RuntimeError: If not connected to the database or if an error occurs during retrieval.
        """
        if not self._connected or not self._connection:
            raise RuntimeError("Not connected to the database.")

        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s;
        """
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, (table_name,))
                columns = cursor.fetchall()
                return [col[0] for col in columns]
        except Exception as e:
            raise RuntimeError(f"Error retrieving columns: {e}") from e
