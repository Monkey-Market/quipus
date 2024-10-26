"""
The `models` module defines the core data models for the application, 
including certificates and templates. These models represent the core entities 
used across the system and are essential for generating, managing, and 
customizing documents like certificates.

Classes:
    Certificate: Represents a certificate entity.
    CertificateFactory: Provides methods for creating certificates.
    Template: Manages HTML templates with associated CSS and assets.
"""

from .certificate import Certificate
from .certificate_factory import CertificateFactory
from .template import Template

__all__ = ['Certificate', 'CertificateFactory', 'Template']
