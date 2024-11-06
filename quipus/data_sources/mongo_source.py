from typing import Optional, override

import polars as pl
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from quipus.data_sources import DataBaseSource
from quipus.utils import DBConfig


class MongoDBSource(DataBaseSource):
    """
    A class for managing connections and data retrieval from a MongoDB
    database using pymongo.

    Attributes:
        connection_string (str): The connection string for the MongoDB
          database.
        collection_name (str): The name of the collection to query.
        query (dict): The query to be executed on the collection.

    Methods:
        initialize_pool(min_connections: int, max_connections: int) -> None:
            Initializes the MongoDB client and sets up connection pooling.

        connect() -> None:
            Establishes a connection to the MongoDB database and sets the connected status.

        disconnect() -> None:
            Closes the MongoDB connection and sets the connection status to disconnected.

        load_data() -> pl.DataFrame:
            Loads data from the MongoDB collection and returns it as a Polars DataFrame.

        get_columns(table_name: str) -> list[str]:
            Retrieves a list of fields from the first document in the specified collection.

        _build_connection_string(db_config: DBConfig, use_srv: bool) -> str:
            Builds a MongoDB connection string based on the given configuration.
    """

    def __init__(
        self,
        collection_name: str,
        query: Optional[dict] = None,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
        use_srv: Optional[bool] = False,
    ):
        """
        Initializes a MongoDBSource instance with the specified parameters.

        Parameters:
            collection_name (str): The name of the collection to query.
            query (Optional[dict], optional): The MongoDB query to execute. Defaults to an empty dictionary.
            connection_string (Optional[str], optional): The connection string for the database.
                Defaults to None, which constructs it from db_config if provided.
            db_config (Optional[DBConfig], optional): A DBConfig instance for constructing the connection string.
                Defaults to None.
            use_srv (Optional[bool], optional): Whether to use the '+srv' scheme for MongoDB. Defaults to False.

        Raises:
            ValueError: If the collection_name is empty or invalid.
        """
        if db_config and not connection_string:
            connection_string = self._build_connection_string(db_config, use_srv)

        super().__init__(connection_string=connection_string, db_config=db_config)
        self.collection_name = collection_name
        self.query = query
        self._client = None
        self._database = None

    @property
    def query(self) -> dict:
        """
        dict: The MongoDB query to be executed.

        Raises:
            ValueError: If the query is not a dictionary.
        """
        return self._query

    @query.setter
    def query(self, value: dict) -> None:
        """
        Sets the MongoDB query.

        Parameters:
            value (dict): The MongoDB query.

        Raises:
            ValueError: If the provided query is not a dictionary.
        """
        if not isinstance(value, dict):
            raise ValueError("The query must be a dictionary.")
        self._query = value

    @property
    def collection_name(self) -> str:
        """
        str: The name of the collection to query.

        Raises:
            ValueError: If the collection name is not a string or is empty.
        """
        return self._collection_name

    @collection_name.setter
    def collection_name(self, value: str) -> None:
        """
        Sets the collection name for the MongoDB query.

        Parameters:
            value (str): The name of the collection.

        Raises:
            ValueError: If the collection name is not a string or is empty.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The collection name must be a non-empty string.")
        self._collection_name = value

    def initialize_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Initializes the connection pool for MongoDB by creating a MongoClient instance.

        MongoDB handles connection pooling automatically, so this method mainly initializes the client.

        Parameters:
            min_connections (int): The minimum number of connections in the pool. Defaults to 1.
            max_connections (int): The maximum number of connections in the pool. Defaults to 10.

        Raises:
            ConnectionError: If the client fails to connect to MongoDB.
        """
        try:
            self._client = MongoClient(
                self.connection_string,
                minPoolSize=min_connections,
                maxPoolSize=max_connections,
            )
            self._client.admin.command("ping")
            self._database = self._client[self.db_config.database]

        except ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}") from e

    def connect(self):
        """
        Establishes a connection to the MongoDB database and sets the connected status.

        Raises:
            ConnectionError: If an error occurs while trying to connect to the database.
        """
        if not self._client:
            self.initialize_pool()

        if self._database is None:
            self._database = self._client[self.db_config.database]

        try:
            self._client.admin.command("ping")
            self._connected = True
        except Exception as e:
            self._connected = False
            raise ConnectionError("Failed to connect to the MongoDB database.") from e

    def disconnect(self):
        """
        Closes the MongoDB client connection and sets the connection status to False.

        Raises:
            RuntimeError: If the MongoDB client is not initialized.
        """
        if not self._client:
            raise RuntimeError("MongoDB client not initialized.")
        self._client.close()
        self._connected = False

    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the specified MongoDB collection based on the query.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the query results.

        Raises:
            ConnectionError: If not connected to the database.
            ValueError: If an error occurs during data loading.
        """
        if not self._connected or self._database is None:
            raise ConnectionError("Not connected to the MongoDB database.")

        collection = self._database[self.collection_name]
        result_cursor = collection.find(self.query)

        result = list(result_cursor)
        return self.to_polars_df(result) if result else pl.DataFrame()

    @override
    def get_columns(self, table_name: str, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of fields from the first document in the specified MongoDB collection.

        Parameters:
            table_name (str): The name of the collection.

        Returns:
            list[str]: A list of field names in the collection.

        Raises:
            ConnectionError: If not connected to the database.
            ValueError: If the collection is empty or does not exist.
        """
        if not self._connected or self._database is None:
            raise ConnectionError("Not connected to the MongoDB database.")

        collection = self._database[table_name]
        document = collection.find_one()

        if not document:
            raise ValueError(f"Collection '{table_name}' is empty or does not exist.")

        return list(document.keys())

    def _build_connection_string(self, db_config: DBConfig, use_srv: bool) -> str:
        """
        Constructs a MongoDB connection string based on the provided configuration.

        Parameters:
            db_config (DBConfig): The database configuration object.
            use_srv (bool): Whether to use the '+srv' scheme for MongoDB.

        Returns:
            str: The constructed connection string.
        """
        scheme = "mongodb+srv" if use_srv else "mongodb"
        if use_srv:
            return f"{scheme}://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}"
        else:
            return f"{scheme}://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
