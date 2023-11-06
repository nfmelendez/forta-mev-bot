from typing import List, Optional

from pydantic import BaseModel

try:
    from src.schemas.events import Protocol
except ModuleNotFoundError:
    from schemas.events import Protocol

class BlockBuilder(BaseModel):
    name: str
    addresses: List[str]
    chain_id: int

