from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ParserResult:
    success: bool = False
    error: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
