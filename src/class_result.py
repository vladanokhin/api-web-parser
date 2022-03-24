from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseResult:
    success: bool = False
    error: Optional[str] = None
    content: Optional[str] = None
