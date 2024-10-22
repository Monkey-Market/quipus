"""
The root module of the library provides a unified API for accessing the main 
components of the library. It includes functionalities for loading data from 
various sources, managing documents (such as certificates), and delivering 
files or documents through email, SFTP, or S3.

Classes:
    CSVDataSource: Loads data from CSV files.
    PostgreSQLDataSource: Loads data from PostgreSQL databases.
    XLSXDataSource: Loads data from XLSX files.
    Certificate: Represents a certificate entity.
    CertificateFactory: Provides methods for creating certificates.
    Template: Manages HTML templates with associated CSS and assets.
    EmailMessageBuilder: Helps in constructing email messages.
    EmailSender: Sends emails via an SMTP server.
    S3Delivery: Uploads files to Amazon S3.
    SFTPDelivery: Transfers files via SFTP.
    SMTPConfig: Configures the SMTP server for sending emails.
    TemplateManager: Manages document templates and integrates them with data sources.
"""

from .data_sources import CSVDataSource, PostgreSQLDataSource, XLSXDataSource
from .models import Certificate, CertificateFactory, Template
from .services import (
    EmailMessageBuilder,
    EmailSender,
    S3Delivery,
    SFTPDelivery,
    SMTPConfig,
    TemplateManager,
)

__all__ = [
    "CSVDataSource",
    "PostgreSQLDataSource",
    "XLSXDataSource",
    "Certificate",
    "CertificateFactory",
    "Template",
    "EmailMessageBuilder",
    "EmailSender",
    "S3Delivery",
    "SFTPDelivery",
    "SMTPConfig",
    "TemplateManager",
]
