from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Certificate:
    completion_date: str
    content: str
    entity: str
    name: str
    duration: Optional[str] = None
    validity_checker: Optional[str] = None
