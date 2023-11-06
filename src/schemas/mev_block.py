from forta_agent import  TransactionEvent, BlockEvent
from pydantic import BaseModel, ConfigDict


class MevBlock(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    number: int = 0
    transactions: [TransactionEvent] = []
    block : BlockEvent = None
