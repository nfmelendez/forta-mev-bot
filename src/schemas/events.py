from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel


class Classification(Enum):
    unknown = "unknown"
    swap = "swap"
    transfer = "transfer"
    liquidate = "liquidate"
    flashloan = "flashloan"


class Protocol(str, Enum):
    uniswap_v2 = "uniswap_v2"
    uniswap_v3 = "uniswap_v3"
    sushiswap = "sushiswap"
    aave = "aave"



class Event(BaseModel):
    block_hash: str
    block_number: int
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    error: Optional[str]
    #event_address: str


class ClassifiedEvent(Event):
    classification: Classification
    to_address: Optional[str] = None
    from_address: Optional[str] = None
    gas: Optional[int] = 0
    value: Optional[int] = 0
    gas_used: Optional[int] = 0
    transaction_hash: str
    transaction_position: int
    protocol: Optional[Protocol] = None
    event_name: Optional[str] = None
    event_signature: Optional[str] = None
    inputs: Optional[Dict[str, Any]] = None
    abi_name: Optional[str] = None
    log_index: int
    emitter_address: str

    class Config:
        validate_assignment = True
        json_encoders = {
            # a little lazy but fine for now
            # this is used for bytes value inputs
            bytes: lambda b: b.hex(),
        }


class CodedEvent(ClassifiedEvent):
    from_address: str


class DecodedEvent(CodedEvent):
    inputs: Dict[str, Any]
    abi_name: str
    protocol: Optional[Protocol]
    gas: Optional[int] = 0
    gas_used: Optional[int] = 0
    event_name: str
    event_signature: str