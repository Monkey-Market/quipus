from typing import Optional, List, Any

from psycopg_pool import ConnectionPool


class PostgreSQLDataSource:
    """
    PostgreSQL DataSource class to manage data retrieval from a PostgreSQL database.

    Attributes:
        host (str): PostgreSQL server host.
        database (str): Name of the database to connect to.
        user (str): Username for authentication.
        password (str): Password for authentication.
        port (int): PostgreSQL server port.
        connection_pool (ConnectionPool): Pool of PostgreSQL connections.
        timeout (Optional[int]): Query execution timeout in seconds.
    """

    def __init__(
        self,
        *,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 5432,
        pool_size: int = 5,
        timeout: int = 15,
    ):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self.__port = port
        self.__timeout = timeout
        self.__connection_pool = self.__initialize_pool(pool_size)

    def __initialize_pool(self, pool_size: int) -> ConnectionPool:
        """
        Initialize the PostgreSQL connection pool.

        Args:
            pool_size (int): Number of connections to keep in the pool.

        Returns:
            ConnectionPool: Initialized connection pool.
        """
        connection_string = (
            f"dbname={self.database} user={self.user} password={self.password} "
            f"host={self.host} port={self.port}"
        )
        return ConnectionPool(
            connection_string,
            min_size=1,
            max_size=pool_size,
        )

    @property
    def host(self) -> str:
        """
        Get the PostgreSQL server host.

        Returns:
            str: PostgreSQL server host.
        """
        return self.__host

    @host.setter
    def host(self, host: str) -> None:
        """
        Set the PostgreSQL server host.

        Args:
            host (str): PostgreSQL server host.

        Raises:
            TypeError: If host is not a string.
            ValueError: If host is an empty string.
        """
        if not isinstance(host, str):
            raise TypeError("'host' must be a string.")
        if not host.strip():
            raise ValueError("'host' cannot be an empty string.")
        self.__host = host

    @property
    def port(self) -> int:
        """
        Get the PostgreSQL server port.

        Returns:
            int: PostgreSQL server port.
        """
        return self.__port

    @port.setter
    def port(self, port: int) -> None:
        """
        Set the PostgreSQL server port.

        Args:
            port (int): PostgreSQL server port.

        Raises:
            TypeError: If port is not an integer.
            ValueError: If port is not between 1 and 65535.
        """
        if not isinstance(port, int):
            raise TypeError("'port' must be an integer.")
        if port not in range(1, 65536):
            raise ValueError("'port' must be between 1 and 65535.")
        self.__port = port

    @property
    def user(self) -> str:
        """
        Get the username for authentication.

        Returns:
            str: Username for authentication.
        """
        return self.__user

    @user.setter
    def user(self, user: str) -> None:
        """
        Set the username for authentication.

        Args:
            user (str): Username for authentication.

        Raises:
            TypeError: If user is not a string.
            ValueError: If user is an empty string.
        """
        if not isinstance(user, str):
            raise TypeError("'user' must be a string.")
        if not user.strip():
            raise ValueError("'user' cannot be an empty string.")
        self.__user = user

    @property
    def password(self) -> str:
        """
        Get the password for authentication.

        Returns:
            str: Password for authentication.
        """
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        """
        Set the password for authentication.

        Args:
            password (str): Password for authentication.

        Raises:
            TypeError: If password is not a string.
            ValueError: If password is an empty string.
        """
        if not isinstance(password, str):
            raise TypeError("'password' must be a string.")
        if not password.strip():
            raise ValueError("'password' cannot be an empty string.")
        self.__password = password

    @property
    def database(self) -> str:
        """
        Get the name of the database to connect to.

        Returns:
            str: Name of the database to connect to.
        """
        return self.__database

    @database.setter
    def database(self, database: str) -> None:
        """
        Set the name of the database to connect to.

        Args:
            database (str): Name of the database to connect to.

        Raises:
            TypeError: If database is not a string.
            ValueError: If database is an empty string.
        """
        if not isinstance(database, str):
            raise TypeError("'database' must be a string.")
        if not database.strip():
            raise ValueError("'database' cannot be an empty string.")
        self.__database = database

    @property
    def timeout(self) -> int:
        """
        Get the query execution timeout in seconds.

        Returns:
            int: Query execution timeout in seconds."""
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        """
        Set the query execution timeout in seconds.

        Args:
            timeout (int): Query execution timeout in seconds.

        Raises:
            TypeError: If timeout is not an integer.
            ValueError: If timeout is not between 0 and 3600 seconds.
        """
        if not isinstance(timeout, int):
            raise TypeError("'timeout' must be an integer.")

        if timeout < 0 or timeout > 3600:
            raise ValueError("'timeout' must be between 0 and 3600 seconds.")

        self.__timeout = timeout

    def close_pool(self) -> None:
        """
        Close the connection pool and release all connections.
        """
        if self.__connection_pool:
            self.__connection_pool.close()

    def fetch_data(self, query: str) -> tuple[List[Any], List[str]]:
        """
        Fetch data from the PostgreSQL database based on the provided query.

        Args:
            query (str): SQL query to execute.

        Returns:
            tuple[List[Any], List[str]]: A tuple containing:
                - List of data rows retrieved from the database.
                - List of column names corresponding to the data.

        Raises:
            ValueError: If no query is provided.
            RuntimeError: If an error occurs during query execution.
        """
        if not query:
            raise ValueError("Query must be provided to fetch data.")

        with self.__connection_pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
                columns = [desc.name for desc in cursor.description]
                return data, columns

    def execute_query(self, query: str) -> Optional[tuple[List[Any], List[str]]]:
        """
        Execute a custom SQL query.

        Args:
            query (str): SQL query to execute.

        Returns:
            Optional[Tuple[List[Any], List[str]]]: A tuple containing:
                - List of data rows retrieved from the database.
                - List of column names corresponding to the data.
                Returns None if no data is returned (e.g., for INSERT, UPDATE, DELETE).

        Raises:
            RuntimeError: If an error occurs during query execution.
        """
        with self.__connection_pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                # Only if the query returns results (e.g., SELECT)
                if cursor.description:
                    data = cursor.fetchall()
                    columns = [desc.name for desc in cursor.description]
                    return data, columns

                # For queries like INSERT, UPDATE, DELETE
                conn.commit()
                return None

    def __str__(self) -> str:
        """
        Get a string representation of the PostgreSQLDataSource object.

        Returns:
            str: String representation of the PostgreSQLDataSource object.
        """
        return (
            f"PostgreSQLDataSource(host={self.host}, port={self.port}, "
            f"database={self.database}, user={self.user})"
        )
