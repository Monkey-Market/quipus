"""
The `data_sources` module provides classes for loading data from various sources, 
including CSV files, PostgreSQL databases, and XLSX files. Each class is designed 
to handle a specific data source, abstracting the complexity of fetching and 
managing data.

Classes:
    CSVDataSource: Class for loading data from CSV files.
    PostgreSQLDataSource: Class for loading data from PostgreSQL databases.
    XLSXDataSource: Class for loading data from XLSX files.
"""

from .csv_data_source import CSVDataSource
from .postgresql_data_source import PostgreSQLDataSource
from .xlsx_data_source import XLSXDataSource


__all__ = ["CSVDataSource", "PostgreSQLDataSource", "XLSXDataSource"]
