from itertools import groupby
from typing import Dict, List

try:
    from src.schemas.events import ClassifiedEvent
except ModuleNotFoundError:
    from schemas.events import ClassifiedEvent



def get_events_by_transaction_hash(
    events: List[ClassifiedEvent],
) -> Dict[str, List[ClassifiedEvent]]:
    get_transaction_hash = lambda e: e.transaction_hash
    return {
        transaction_hash: list(events)
        for transaction_hash, events in groupby(
            sorted(events, key=get_transaction_hash),
            key=get_transaction_hash,
        )
    }
