from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Certificate:
    """
    Data class to represent a certificate
    
    Attributes:
        completion_date (str): the date the certificate was completed
        content (str): the content of the certificate
        entity (str): the entity that issued the certificate
        name (str): the name of the certificate
        duration (Optional[str]): the duration of the certificate
        validity_checker (Optional[str]): the validity checker of the certificate
    """
    completion_date: str
    content: str
    entity: str
    name: str
    duration: Optional[str] = None
    validity_checker: Optional[str] = None
