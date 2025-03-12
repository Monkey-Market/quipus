"""
The root module of the library provides a unified API for accessing the main 
components and functionalities of the library. It includes tools for loading data 
from various sources, managing document templates, and delivering documents 
through different services such as email, SFTP, or Amazon S3.

Classes and Components:
    AWSConfig: Configuration class for AWS services.
    Connectable: Abstract base class for connectable data sources.
    CSVSource: Class for loading data from CSV files.
    DataBaseSource: Abstract base class for database sources.
    DBConfig: Configuration class for database connections.
    EmailMessageBuilder: Helper class for constructing email messages.
    EmailSender: Class for sending emails via an SMTP server.
    EncodingType: Enum for file encoding types.
    ReplacementsDict: TypedDict for template replacements validation.
    ValidReplacementValue: Union type for valid replacement values.
    FileSource: Abstract base class for file-based data sources.
    MongoDBSource: Class for connecting to and loading data from MongoDB databases.
    MySQLSource: Class for connecting to and loading data from MySQL databases.
    ParquetSource: Class for loading data from Parquet files.
    PostgreSQLSource: Class for connecting to and loading data from PostgreSQL databases.
    S3Delivery: Class for uploading files to Amazon S3.
    SFTPDelivery: Class for transferring files via SFTP.
    SMTPConfig: Configuration class for SMTP server settings.
    Template: Class for managing HTML templates with associated assets and CSS.
    TemplateManager: Class for managing and integrating document templates with data sources.
    XLSXSource: Class for loading data from XLSX files.
"""

from .data_sources import (
    CSVDataSource,
    CSVSource,
    DataBaseSource,
    DataSource,
    FileSource,
    MongoDBSource,
    MySQLSource,
    ParquetSource,
    PostgreSQLSource,
    XLSXSource,
)
from .models import Template
from .services import (
    AWSConfig,
    EmailMessageBuilder,
    EmailSender,
    S3Delivery,
    SFTPDelivery,
    SMTPConfig,
    TemplateManager,
)
from .utils import (
    Connectable,
    DBConfig,
    EncodingType,
    ReplacementsDict,
    ValidReplacementValue,
)

__all__ = [
    "AWSConfig",
    "Connectable",
    "CSVDataSource",
    "CSVSource",
    "DataBaseSource",
    "DataSource",
    "DBConfig",
    "EmailMessageBuilder",
    "EmailSender",
    "EncodingType",
    "ReplacementsDict",
    "ValidReplacementValue",
    "FileSource",
    "MongoDBSource",
    "MySQLSource",
    "ParquetSource",
    "PostgreSQLSource",
    "S3Delivery",
    "SFTPDelivery",
    "SMTPConfig",
    "Template",
    "TemplateManager",
    "XLSXSource",
]
