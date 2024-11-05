from dataclasses import dataclass
from typing import Optional


@dataclass
class DBConfig:
    """
    Data class for database configuration.

    Attributes:
        host (str): The hostname or IP address of the database server.
        user (str): The username for authentication.
        password (str): The password for authentication.
        port (int): The port number to connect to.
        database (str): The name of the database to connect to.
    """

    host: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
