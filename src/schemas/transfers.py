from typing import List, Optional

from pydantic import BaseModel


class Transfer(BaseModel):
    block_number: int
    transaction_hash: str
    from_address: str
    to_address: str
    amount: int
    token_address: str
    log_index: int
    tokenId: Optional[int] = -1
