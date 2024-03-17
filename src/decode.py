from typing import Dict, Optional, List
import logging

import eth_utils.abi
from eth_abi import decode_abi
from eth_abi.exceptions import InsufficientDataBytes, NonEmptyPaddingBytes
from hexbytes._utils import hexstr_to_bytes


try:
    from src.schemas.abi import ABI, ABIFunctionDescription, ABIEventDescription
except ModuleNotFoundError:
    from schemas.abi import ABI, ABIFunctionDescription, ABIEventDescription



from typing import Any, Dict

from pydantic import BaseModel

from forta_agent import Log


class EventData(BaseModel):
    event_name: str
    event_signature: str
    inputs: Dict[str, Any]


# 0x + 8 characters
SELECTOR_LENGTH = 10


class ABIDecoder:
    def __init__(self, abi: ABI):
        self._functions_by_selector: Dict[str, ABIFunctionDescription] = {
            description.get_selector(): description
            for description in abi
            if isinstance(description, ABIFunctionDescription)
        }
        self._events_by_selector: Dict[str, ABIEventDescription] = {
            description.get_selector(): description
            for description in abi
            if isinstance(description, ABIEventDescription)
        }

    def decode(self, event_log: Log) -> Optional[EventData]:

        # in polygon can exist event log without topics, therefore no signature but with data.
        if not event_log.topics:
            return None

        topics_hex = [t[2:] for t in event_log.topics[1:]]
        data_hex = [event_log.data[2:]]
        topics = "".join(topics_hex)
        data = "".join(data_hex)

        try:
            selector = event_log.topics[0][:SELECTOR_LENGTH]
        except:
            logging.error(f"Error in  decode, event_log.topics[0][:SELECTOR_LENGTH] {event_log.block_number} {event_log.transaction_hash}")
            return None

        evt = self._events_by_selector.get(selector)

        if evt is None:
            return None
        indexed_inputs = []
        basic_inputs = []
        indexed_inputs = self.get_indexed_event_inputs(evt.inputs)
        basic_inputs = self.basic_event_inputs(evt.inputs)
        try:
            if len(topics_hex) == len(indexed_inputs):
                topics_dict = self._decode(indexed_inputs, topics)
            else:
                return None
            data_dict = self._decode(basic_inputs, data)
        except InsufficientDataBytes as idb:
            return None
        except NonEmptyPaddingBytes as nepb:
            return None
        except OverflowError as oe:
            return None

        inputs_result = {**topics_dict, **data_dict}
        return EventData(
            event_name=evt.name,
            event_signature=evt.get_signature(),
            inputs= inputs_result
        )
    

    def get_indexed_event_inputs(self, event_description: [ABIEventDescription]) -> List[ABIEventDescription]:
        return [arg for arg in event_description if arg.indexed is True]
    
    def basic_event_inputs(self, event_description: [ABIEventDescription]) -> List[ABIEventDescription]:
        return [arg for arg in event_description if arg.indexed is False]
    
    def _decode(self, inputs, params):
        if not inputs or params == '':
            return {}
        
        names = [input.name for input in inputs]
        types = [
            input.type
            if not input.type.startswith("tuple")
            else eth_utils.abi.collapse_if_tuple(input.dict())
            for input in inputs
        ]

        decoded = decode_abi(types, hexstr_to_bytes(params))

        return {name: value for name, value in zip(names, decoded)}
