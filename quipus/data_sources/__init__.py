"""
The `data_sources` module provides classes for loading data from a variety of sources, 
including CSV files, XLSX files, Parquet files, and databases such as PostgreSQL, MongoDB, 
and MySQL. Each class abstracts the complexity of data retrieval, allowing users to easily 
interact with and load data from different sources.

Classes:
    FileSource: Abstract base class for file-based data sources.
    CSVSource: Class for loading data from CSV files.
    XLSXSource: Class for loading data from XLSX files.
    ParquetSource: Class for loading data from Parquet files.
    DataBaseSource: Abstract base class for database sources.
    PostgreSQLSource: Class for connecting to and loading data from PostgreSQL databases.
    MongoDBSource: Class for connecting to and loading data from MongoDB databases.
    MySQLSource: Class for connecting to and loading data from MySQL databases.
"""

from .data_source import DataSource

from .file_source import FileSource
from .csv_source import CSVSource
from .xlsx_source import XLSXSource
from .parquet_source import ParquetSource

from .database_source import DataBaseSource
from .postgre_source import PostgreSQLSource
from .mongo_source import MongoDBSource
from .mysql_source import MySQLSource

# Deprecated
from .csv_data_source import CSVDataSource

__all__ = [
    "DataSource",
    "FileSource",
    "CSVSource",
    "XLSXSource",
    "ParquetSource",
    "DataBaseSource",
    "PostgreSQLSource",
    "MongoDBSource",
    "MySQLSource",

    # Deprecated
    "CSVDataSource",
]
