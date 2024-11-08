from abc import ABC, abstractmethod
from typing import Optional


class Connectable(ABC):
    """
    An abstract base class representing a connectable entity.

    This class provides the structure for defining objects that can establish and manage
    connections, supporting the context management protocol to ensure proper resource handling.

    Attributes:
        connection_string (str): The connection string used for establishing a connection.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
    ):
        """
        Initializes a new instance of the Connectable class.

        Args:
            connection_string (Optional[str]): The connection string for the connectable object.
        """
        self.connection_string = connection_string
        self._connection_pool = None

    def __enter__(self):
        """
        Enters a runtime context related to this object, establishing a connection.

        Returns:
            Connectable: The current instance of the class.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits the runtime context, ensuring the connection is properly closed.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The exception instance.
            traceback (TracebackType): The traceback object.
        """
        self.disconnect()

    @property
    def connection_string(self) -> str:
        """
        str: The connection string for the connectable object.

        Raises:
            ValueError: If the connection string is not a string or is empty.
        """
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value: str) -> None:
        """
        Sets the connection string for the connectable object.

        Args:
            value (str): The new connection string.

        Raises:
            ValueError: If the provided value is not a string or is empty.
        """
        if not isinstance(value, str):
            raise ValueError("The connection string must be a string.")
        if value.strip() == "":
            raise ValueError("The connection string cannot be empty.")
        self._connection_string = value

    @abstractmethod
    def connect(self) -> None:
        """
        Establishes a connection to the target resource.

        This method must be implemented by any subclass.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """
        Terminates the connection to the target resource.

        This method must be implemented by any subclass.
        """

    @abstractmethod
    def initialize_pool(self, min_connections: int, max_connections: int) -> None:
        """
        Initializes a connection pool for the connectable object.

        Args:
            min_connections (int): The minimum number of connections in the pool.
            max_connections (int): The maximum number of connections in the pool.

        This method must be implemented by any subclass.
        """
