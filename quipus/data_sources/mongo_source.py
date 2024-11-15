from typing import Optional, override

import polars as pl
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from quipus.utils import DBConfig

from .database_source import DataBaseSource


class MongoDBSource(DataBaseSource):
    """
    A class for managing connections and data retrieval from a MongoDB
    database using pymongo.

    Attributes:
        connection_string (str): The connection string for the MongoDB
          database.
        collection_name (str): The name of the collection to query.
        query (dict): The query to be executed on the collection.
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
            query (Optional[dict]): The MongoDB query to execute. Defaults to an empty dictionary.
            connection_string (Optional[str]): The connection string for the database.
                Defaults to None, which constructs it from db_config if provided.
            db_config (Optional[DBConfig]): A DBConfig instance for constructing
              the connection string. Defaults to None.
            use_srv (Optional[bool]): Whether to use the '+srv' scheme for MongoDB.
              Defaults to False.

        Raises:
            ValueError: If neither db_config nor connection_string is provided.
            ValueError: If the collection_name is empty or invalid.
        """
        if not db_config and not connection_string:
            raise ValueError("Either db_config or connection_string must be provided.")

        if db_config and not connection_string:
            connection_string = self._build_connection_string(db_config, use_srv)

        if not db_config and connection_string:
            self.db_config.database = connection_string.split("/")[-1]

        super().__init__(connection_string=connection_string, db_config=db_config)
        self.collection_name = collection_name
        self.query = query
        self._client = None
        self._database = None
        self.connected = False

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

    @override
    def initialize_pool(self, min_connections: int = 1, max_connections: int = 10):
        """
        Initializes the connection pool for MongoDB by creating a MongoClient instance.

        MongoDB handles connection pooling automatically, this method only initializes the client.

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

    @override
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
            self.connected = True
        except Exception as e:
            self.connected = False
            raise ConnectionError("Failed to connect to the MongoDB database.") from e

    @override
    def disconnect(self):
        """
        Closes the MongoDB client connection and sets the connection status to False.

        Raises:
            RuntimeError: If the MongoDB client is not initialized.
        """
        if not self._client:
            raise RuntimeError("MongoDB client not initialized.")
        self._client.close()
        self.connected = False

    @override
    def load_data(self) -> pl.DataFrame:
        """
        Loads data from the specified MongoDB collection based on the query.

        Returns:
            pl.DataFrame: A Polars DataFrame containing the query results.

        Raises:
            ConnectionError: If not connected to the database.
            ValueError: If an error occurs during data loading.
        """
        if not self.connected or self._database is None:
            raise ConnectionError("Not connected to the MongoDB database.")

        collection = self._database[self.collection_name]
        result_cursor = collection.find(self.query)

        result = list(result_cursor)
        return self.to_polars_df(result) if result else pl.DataFrame()

    @override
    def get_columns(self, *args, **kwargs) -> list[str]:
        """
        Retrieves the list of fields from the first document in the specified MongoDB collection.

        Parameters:
            table_name (str): The name of the collection.

        Returns:
            list[str]: A list of field names in the collection.

        Raises:
            ConnectionError: If not connected to the database.
            ValueError: If the collection is empty or does not exist.
            ValueError: If the table_name is not provided.
        """
        if not self.connected or self._database is None:
            raise ConnectionError("Not connected to the MongoDB database.")

        table_name = args[0] if args else kwargs.get("table_name")
        if not table_name:
            raise ValueError("Table name must be provided.")

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
            return (
                f"{scheme}://{db_config.user}:{db_config.password}@"
                f"{db_config.host}/{db_config.database}"
            )

        return (
            f"{scheme}://{db_config.user}:{db_config.password}@"
            f"{db_config.host}:{db_config.port}/{db_config.database}"
        )
