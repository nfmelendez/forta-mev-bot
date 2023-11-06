from typing import List, Optional

from pydantic import BaseModel

try:
    from src.schemas.events import Protocol
except ModuleNotFoundError:
    from schemas.events import Protocol

class FlashLoan(BaseModel):
    abi_name: str
    transaction_hash: str
    transaction_position: int
    block_number: int
    log_index: int
    contract_address: str
    from_address: str
    to_address: str
    protocol: Protocol
    target: str
    initiator: str
    asset: str
    amount: int
    premium: int
    referralCode: int
    error: Optional[str]
