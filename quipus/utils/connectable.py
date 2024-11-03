from abc import ABC, abstractmethod


class Connectable(ABC):
    """
    Abstract class for connectable objects.

    Methods:
        connect: Connect to the object.
        disconnect: Disconnect from the object.
        initialize_pool: Initialize a connection pool for the object.
    """

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def initialize_pool(self, min_connections: int, max_connections: int) -> None: ...
