from typing import Optional

from quipus.utils import Connectable, DBConfig

from .data_source import DataSource


class DataBaseSource(DataSource, Connectable):
    """
    An abstract base class for database sources.

    Attributes:
        connected (bool): Indicates whether the source is currently connected to the database.
            Default is False.
        db_config (DBConfig): The database connection configuration and credentials.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_config: Optional[DBConfig] = None,
    ):
        """
        Initializes a DataBaseSource instance.

        Parameters:
            connection_string (Optional[str]): The connection string for the database.
                Defaults to None.
            db_config (Optional[DBConfig]): The database connection configuration.
                Defaults to None.

        Raises:
            ValueError: If neither a connection string nor a DBConfig object is provided.
        """
        if not connection_string and not db_config:
            raise ValueError("A connection string or DBConfig must be provided.")

        if connection_string:
            super().__init__(connection_string)

        self.db_config = db_config
        self.connected = False

    @property
    def connected(self) -> bool:
        """
        bool: Indicates whether the source is connected to the database.

        Raises:
            TypeError: If the value set is not a boolean.
        """
        return self._connected

    @connected.setter
    def connected(self, value: bool) -> None:
        """
        Sets the connection status of the database source.

        Parameters:
            value (bool): The new connection status.

        Raises:
            TypeError: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("The connected attribute must be a boolean.")
        self._connected = value
