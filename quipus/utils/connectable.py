from abc import ABC, abstractmethod
from typing import Optional


class Connectable(ABC):
    """
    Abstract class for connectable objects.

    Attributes:
        connection_string: The connection string for the object.

    Methods:
        connect: Connect to the object.
        disconnect: Disconnect from the object.
        initialize_pool: Initialize a connection pool for the object.
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
    ):
        self.connection_string = connection_string

    @property
    def connection_string(self) -> str:
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The connection string must be a string.")
        if value.strip() == "":
            raise ValueError("The connection string cannot be empty.")
        self._connection_string = value

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def initialize_pool(self, min_connections: int, max_connections: int) -> None: ...
