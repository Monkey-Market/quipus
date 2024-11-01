"""
The `models` module defines the core data models for the application, 
including templates. These models represent the core entities 
used across the system and are essential for generating, managing, and 
customizing documents like invoices.

Classes:
    Template: Manages HTML templates with associated CSS and assets.
"""

from .template import Template

__all__ = ["Template"]
