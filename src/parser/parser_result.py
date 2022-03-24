from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.class_result import BaseResult


@dataclass
class ParserResult(BaseResult):
    metadata: Optional[Dict[str, Any]] = None
