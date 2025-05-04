from pydantic import BaseModel
from typing import Dict, Tuple


class BootstrapResponseDTO(BaseModel):
    results: Dict[str, Tuple[int, int]]
    message: str
