"""
This module aggregates and exports core components related to 
database connections and configurations.

It includes:
- EncodingType: Enum representing the type of encoding used for data
 processing.
- Connectable: Abstract base class for defining connectable objects.
- DBConfig: Class that handles database configuration settings.

Exports:
    EncodingType: Enum class for encoding types.
    Connectable: Abstract base class for connectable resources.
    DBConfig: Class for managing database configuration.
"""

from .connectable import Connectable
from .dbconfig import DBConfig
from .types import EncodingType

__all__ = ["EncodingType", "Connectable", "DBConfig"]
