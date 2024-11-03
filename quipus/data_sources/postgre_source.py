from psycopg_pool import ConnectionPool
from .database_source import DataBaseSource

import polars as pl


class PostgreSQLSource(DataBaseSource):
    """
    Class for managing connections to a PostgreSQL database using psycopg v3 and connection pooling.

    Attributes:
        connection_string (str): The connection string for the PostgreSQL database.
        query: The query to execute on the database.
    """

    def __init__(self, connection_string: str, query: str):
        super().__init__(connection_string)
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

    @classmethod
    def build_connection_string(
        cls, user: str, password: str, host: str, port: int, database: str
    ) -> str:
        """
        Builds a PostgreSQL connection string from the provided parameters.

        Args:
            user (str): The username for authentication.
            password (str): The password for authentication.
            host (str): The hostname or IP address of the database server.
            port (int): The port number to connect to (default for PostgreSQL is 5432).
            database (str): The name of the database to connect to.

        Returns:
            str: The connection string for the PostgreSQL database.

        Example:
            >>> connection_string = PostgreSQLSource.build_connection_string(
            ...     user="myuser", password="mypassword", host="localhost", port=5432, database="mydatabase"
            ... )
            >>> print(connection_string) # 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
        """
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def initialize_pool(
        self, min_connections: int = 1, max_connections: int = 10
    ) -> None:
        """
        Initializes the connection pool for PostgreSQL.

        Args:
            min_connections (int): The minimum number of connections in the pool.
            max_connections (int): The maximum number of connections in the pool.
        """
        try:
            self._connection_pool = ConnectionPool(
                conninfo=self.connection_string,
                min_size=min_connections,
                max_size=max_connections,
            )
            if not self._connection_pool:
                raise RuntimeError("Failed to create the connection pool.")
        except Exception as e:
            raise RuntimeError(f"Error initializing connection pool: {e}")

    def connect(self) -> None:
        """Obtains a connection from the pool and sets the connected status to True."""
        if not self._connection_pool:
            raise RuntimeError("Connection pool not initialized.")
        try:
            self._connection = self._connection_pool.getconn()
            self._connection.autocommit = True
            self._connected = True
        except Exception as e:
            raise RuntimeError(f"Error connecting to the database: {e}")

    def disconnect(self) -> None:
        """Releases the connection back to the pool and sets the connected status to False."""
        if self._connected and self._connection:
            try:
                self._connection_pool.putconn(self._connection)
                self._connected = False
            except Exception as e:
                raise RuntimeError(f"Error disconnecting from the database: {e}")
        else:
            raise RuntimeError("No active connection to disconnect.")

    def load_data(self) -> pl.DataFrame:
        """
        Executes a query to load data from the PostgreSQL database.

        Returns:
            Any: The result of the query as a list of tuples.

        Raises:
            RuntimeError: If an error occurs while loading the data.
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
            raise RuntimeError(f"Error loading data: {e}")

    def get_columns(self, table_name: str) -> list[str]:
        """
        Retrieves the list of columns from a specific table in the PostgreSQL database.

        Args:
            table_name (str): The name of the table.

        Returns:
            list[str]: A list of column names.
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
            raise RuntimeError(f"Error retrieving columns: {e}")
