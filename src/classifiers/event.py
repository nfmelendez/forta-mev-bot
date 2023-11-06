
from pydantic import BaseModel
from typing import List, Dict
from forta_agent import  TransactionEvent, Log


try:
    from src.abi import get_abi
    from src.decode import ABIDecoder, EventData
    from src.classifiers.specs import ALL_CLASSIFIER_SPECS
    from src.schemas.events import (
        Classification,
        ClassifiedEvent,
        CodedEvent,
        DecodedEvent
    )
except ModuleNotFoundError:
    from abi import get_abi
    from decode import ABIDecoder
    from classifiers.specs import ALL_CLASSIFIER_SPECS
    from schemas.events import (
        Classification,
        ClassifiedEvent,
        CodedEvent,
        DecodedEvent
    )



class EventLogClassifier:

    def __init__(self) -> None:
        self._classifier_specs = ALL_CLASSIFIER_SPECS
        self._decoders_by_abi_name: Dict[str, ABIDecoder] = {}

        for spec in self._classifier_specs:
            abi = get_abi(spec.abi_name, spec.protocol)

            if abi is None:
                raise ValueError(f"No ABI found for {spec.abi_name}")

            decoder = ABIDecoder(abi)
            self._decoders_by_abi_name[spec.abi_name] = decoder

    def classify(self, transactions: List[TransactionEvent] ) -> List[ClassifiedEvent]:
        result = []
        for t in transactions:
            for event_log in t.logs:
                result.append(self._classify_event_log(t, event_log))

        return result


    def _classify_event_log(self, t: TransactionEvent,  event_log: Log):        
        for spec in self._classifier_specs:
            if spec.valid_contract_addresses is not None:
                lower_valid_addresses = {
                    address.lower() for address in spec.valid_contract_addresses
                }

                if t.to not in lower_valid_addresses:
                    continue
            decoder = self._decoders_by_abi_name[spec.abi_name]
            event_data: EventData = decoder.decode(event_log)

            if event_data is not None:
                signature = event_data.event_signature
                classifier = spec.classifiers.get(signature)
                classification = (
                    Classification.unknown
                    if classifier is None
                    else classifier.get_classification()
                )

                return DecodedEvent(
                    classification=classification,
                    protocol=spec.protocol,
                    abi_name=spec.abi_name,
                    event_name= event_data.event_name,
                    event_signature=signature,
                    inputs=event_data.inputs,
                    to_address=t.to,
                    from_address=t.from_,
                    value=t.transaction.value,
                    block_hash = t.block_hash,
                    block_number = t.block_number,
                    transaction_hash= t.hash,
                    transaction_position=event_log.transaction_index,
                    error=None,
                    log_index=event_log.log_index,
                    emitter_address=event_log.address
                )

        return CodedEvent(
            classification=Classification.unknown,
            to_address=t.to,
            from_address=t.from_,
            value=t.transaction.value,
            block_hash = t.block_hash,
            block_number = t.block_number,
            transaction_hash= t.hash,
            transaction_position=event_log.transaction_index,
            error=None,
            log_index=event_log.log_index,
            emitter_address=event_log.address
        )


