"""
The root module of the library provides a unified API for accessing the main 
components and functionalities of the library. It includes tools for loading data 
from various sources, managing document templates, and delivering documents 
through different services such as email, SFTP, or Amazon S3.

Classes and Components:
    EncodingType: Enum for file encoding types.
    Connectable: Abstract base class for connectable data sources.
    DBConfig: Configuration class for database connections.
    FileSource: Abstract base class for file-based data sources.
    CSVSource: Class for loading data from CSV files.
    XLSXSource: Class for loading data from XLSX files.
    ParquetSource: Class for loading data from Parquet files.
    DataBaseSource: Abstract base class for database sources.
    PostgreSQLSource: Class for connecting to and loading data from PostgreSQL databases.
    MongoDBSource: Class for connecting to and loading data from MongoDB databases.
    MySQLSource: Class for connecting to and loading data from MySQL databases.
    Template: Class for managing HTML templates with associated assets and CSS.
    EmailMessageBuilder: Helper class for constructing email messages.
    EmailSender: Class for sending emails via an SMTP server.
    AWSConfig: Configuration class for AWS services.
    S3Delivery: Class for uploading files to Amazon S3.
    SFTPDelivery: Class for transferring files via SFTP.
    SMTPConfig: Configuration class for SMTP server settings.
    TemplateManager: Class for managing and integrating document templates with data sources.
"""

from .utils import EncodingType, Connectable, DBConfig
from .data_sources import (
    DataSource,
    FileSource,
    CSVSource,
    XLSXSource,
    ParquetSource,
    DataBaseSource,
    PostgreSQLSource,
    MongoDBSource,
    MySQLSource,
    CSVDataSource,
)
from .models import Template
from .services import (
    EmailMessageBuilder,
    EmailSender,
    AWSConfig,
    S3Delivery,
    SFTPDelivery,
    SMTPConfig,
    TemplateManager,
)

__all__ = [
    # utils
    "EncodingType",
    "Connectable",
    "DBConfig",
    # data sources
    "DataSource",
    # file sources
    "FileSource",
    "CSVSource",
    "XLSXSource",
    "ParquetSource",
    # database sources
    "DataBaseSource",
    "PostgreSQLSource",
    "MongoDBSource",
    "MySQLSource",
    # models
    "Template",
    # services
    "EmailMessageBuilder",
    "EmailSender",
    "AWSConfig",
    "S3Delivery",
    "SFTPDelivery",
    "SMTPConfig",
    "TemplateManager",
    "CSVDataSource",
]
