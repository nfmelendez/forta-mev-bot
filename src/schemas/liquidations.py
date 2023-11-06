from typing import List, Optional

from pydantic import BaseModel


try:
    from src.schemas.events import Protocol
except ModuleNotFoundError:
    from schemas.events import Protocol

class Liquidation(BaseModel):
    liquidated_user: str
    liquidator_user: str
    debt_token_address: str
    debt_purchase_amount: int
    received_amount: int
    received_token_address: Optional[str]
    protocol: Protocol
    transaction_hash: str
    log_index: int
    block_number: int
    error: Optional[str] = ""
    receive_a_token: bool
    bot_owner: str
