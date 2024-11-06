"""
The `data_sources` module provides classes for loading data from a variety of sources, 
including CSV files, XLSX files, Parquet files, and databases such as PostgreSQL, MongoDB, 
and MySQL. Each class abstracts the complexity of data retrieval, allowing users to easily 
interact with and load data from different sources.

Classes:
    CSVSource: Class for loading data from CSV files.
    DataBaseSource: Abstract base class for database sources.
    FileSource: Abstract base class for file-based data sources.
    MongoDBSource: Class for connecting to and loading data from MongoDB databases.
    MySQLSource: Class for connecting to and loading data from MySQL databases.
    ParquetSource: Class for loading data from Parquet files.
    PostgreSQLSource: Class for connecting to and loading data from PostgreSQL databases.
    XLSXSource: Class for loading data from XLSX files.
"""

from .csv_data_source import CSVDataSource  # Deprecated
from .csv_source import CSVSource
from .data_source import DataSource
from .database_source import DataBaseSource
from .file_source import FileSource
from .mongo_source import MongoDBSource
from .mysql_source import MySQLSource
from .parquet_source import ParquetSource
from .postgre_source import PostgreSQLSource
from .xlsx_source import XLSXSource

__all__ = [
    "CSVDataSource",  # Deprecated
    "CSVSource",
    "DataBaseSource",
    "DataSource",
    "FileSource",
    "MongoDBSource",
    "MySQLSource",
    "ParquetSource",
    "PostgreSQLSource",
    "XLSXSource",
]
