"""
The `data_sources` module provides classes for loading data from various sources, 
including CSV files, pandas DataFrames, PostgreSQL databases, and XLSX files. Each class is designed to handle a specific data source, abstracting the complexity of fetching and 
managing data.

Classes:
    CSVDataSource: Class for loading data from CSV files.
    DataFrameDataSource: Class for loading data from pandas DataFrames.
    PostgreSQLDataSource: Class for loading data from PostgreSQL databases.
    XLSXDataSource: Class for loading data from XLSX files.
"""

from .csv_data_source import CSVDataSource
from .dataframe_data_source import DataFrameDataSource
from .postgresql_data_source import PostgreSQLDataSource
from .xlsx_data_source import XLSXDataSource


__all__ = [
    "CSVDataSource",
    "DataFrameDataSource",
    "PostgreSQLDataSource",
    "XLSXDataSource",
]
