from typing import List, Optional

from pydantic import BaseModel


try:
    from src.schemas.events import Protocol
except ModuleNotFoundError:
    from schemas.events import Protocol

class Swap(BaseModel):
    abi_name: str
    transaction_hash: str
    transaction_position: int
    block_number: int
    log_index: Optional[int] = -1
    contract_address: str
    from_address: str # address that is sending the assets
    to_address: str # address that is reciving the assets. sometimes could be the same as from_address
    token_in_address: str
    token_in_amount: int
    token_out_address: str
    token_out_amount: int
    protocol: Protocol
    error: Optional[str]
    owner_address: Optional[str] = ""
