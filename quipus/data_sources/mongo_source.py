from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .database_source import DataBaseSource

import polars as pl


class MongoDBSource(DataBaseSource):
    """
    Class for managing connections to a MongoDB database using pymongo.

    Attributes:
        connection_string: The connection string for the MongoDB database.
        database_name: The name of the database to connect to.
        collection_name: The name of the collection to query from.
        query: The query to execute on the collection.
    """

    def __init__(
        self,
        connection_string: str,
        database_name: str,
        collection_name: str,
        query: Optional[dict] = {},
    ):
        super().__init__(connection_string)
        self._client = None
        self._database = None
        self.database_name = database_name
        self.collection_name = collection_name
        self.query = query

    @property
    def query(self) -> dict:
        return self._query

    @query.setter
    def query(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise ValueError("The query must be a dictionary.")
        self._query = value

    @property
    def database_name(self) -> str:
        return self._database_name

    @database_name.setter
    def database_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The database name must be a string.")
        if value.strip() == "":
            raise ValueError("The database name cannot be empty.")
        self._database_name = value

    @property
    def collection_name(self) -> str:
        return self._collection_name

    @collection_name.setter
    def collection_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The collection name must be a string.")
        if value.strip() == "":
            raise ValueError("The collection name cannot be empty.")
        self._collection_name = value

    @classmethod
    def build_connection_string(
        cls,
        host: str,
        port: Optional[int] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        use_srv: bool = False,
        options: Optional[dict[str, str]] = None,
    ) -> str:
        """
        Builds a MongoDB connection string from the provided parameters.

        Args:
            host (str): The hostname or IP address of the MongoDB server.
            port (int, optional): The port number to connect to (default for MongoDB is 27017).
            database (str, optional): The name of the database to connect to.
            user (str, optional): The username for authentication.
            password (str, optional): The password for authentication.
            use_srv (bool, optional): Whether to use the SRV protocol for clusters.
            options (dict, optional): Additional connection options as key-value pairs.

        Returns:
            str: The connection string for the MongoDB database.

        Example:
            >>> connection_string = MongoDBSource.build_connection_string(
            ...     user="admin", password="password", host="localhost", port=27017, database="mydatabase"
            ... )
            >>> print(connection_string) # mongodb://admin:password@localhost:27017/mydatabase

            >>> connection_string = MongoDBSource.build_connection_string(
            ...     host="cluster0-abcde.mongodb.net", user="admin", password="password", use_srv=True
            ... )
            >>> print(connection_string) # mongodb+srv://admin:password
        """
        protocol = "mongodb+srv" if use_srv else "mongodb"
        credentials = f"{user}:{password}@" if user and password else ""
        port_str = f":{port}" if port and not use_srv else ""
        db_str = f"/{database}" if database else ""
        options_str = ""

        if options:
            options_str = "?" + "&".join(
                f"{key}={value}" for key, value in options.items()
            )

        return f"{protocol}://{credentials}{host}{port_str}{db_str}{options_str}"

    def initialize_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Initializes the connection pool for MongoDB.

        MongoDB typically handles connection pooling automatically, so this method simply initializes the client.

        Args:
            min_connections (int): The minimum number of connections in the pool.
            max_connections (int): The maximum number of connections in the pool.
        """
        try:
            self._client = MongoClient(
                self.connection_string,
                minPoolSize=min_connections,
                maxPoolSize=max_connections,
            )
            self._client.admin.command("ping")
            self._database = self._client[self.database_name]

        except ConnectionFailure as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {e}")

    def connect(self):
        """Sets the connection status to True if the client is initialized."""
        try:
            if self._client is not None:
                self._client.admin.command("ping")
                if self._database is not None:
                    self._connected = True
                else:
                    raise RuntimeError("Database instance not found.")
            else:
                raise RuntimeError(
                    "MongoDB client not initialized. Call `initialize_pool()` first."
                )
        except Exception as e:
            self._connected = False
            raise RuntimeError("Failed to connect to the MongoDB database.") from e

    def disconnect(self):
        """Closes the MongoDB client connection and sets the connection status to False."""
        if self._client:
            self._client.close()
            self._is_connected = False
        else:
            raise RuntimeError("MongoDB client not initialized.")

    def load_data(self) -> pl.DataFrame:
        """
        Loads data from a MongoDB collection.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the query results.
        """
        if not self._connected or self._client is None or self._database is None:
            raise RuntimeError("Not connected to the MongoDB database.")

        collection = self._database[self.collection_name]
        result_cursor = collection.find(
            self.query,
        )

        # if limit > 0:
        #     result_cursor = result_cursor.limit(limit)

        result = list(result_cursor)

        if result:
            return self.to_polars_df(result)
        else:
            return pl.DataFrame()

    def get_columns(self) -> list[str]:
        """
        Retrieves the list of fields from the first document in the collection.

        Returns:
            list[str]: The list of fields in the collection.
        """
        if not self._connected or self._database is None:
            raise RuntimeError("Not connected to the MongoDB database.")

        collection = self._database[self.collection_name]
        document = collection.find_one()

        if document:
            return list(document.keys())
        else:
            raise RuntimeError(
                f"Collection '{self.collection_name}' is empty or does not exist."
            )
