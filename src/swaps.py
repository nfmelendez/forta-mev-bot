from typing import List, Optional



try:
    from src.classifiers.specs import get_classifier
    from src.schemas.classifiers import SwapClassifier
    from src.schemas.swaps import Swap
    from src.schemas.events import Classification, ClassifiedEvent, DecodedEvent
    from src.schemas.transfers import Transfer
    from src.events import get_events_by_transaction_hash
    from src.transfers import (
        get_transfer,
    )
except ModuleNotFoundError:
    from classifiers.specs import get_classifier
    from schemas.classifiers import SwapClassifier
    from schemas.swaps import Swap
    from schemas.events import Classification, ClassifiedEvent, DecodedEvent
    from schemas.transfers import Transfer
    from events import get_events_by_transaction_hash
    from transfers import (
        get_transfer,
    )


def get_swaps(events: List[ClassifiedEvent]) -> List[Swap]:
    swaps = []

    for _, transaction_events in get_events_by_transaction_hash(events).items():
        swaps += _get_swaps_for_transaction(list(transaction_events))

    return swaps


def _get_swaps_for_transaction(events: List[ClassifiedEvent]) -> List[Swap]:
    ordered_events = list(sorted(events, key=lambda t: t.log_index))

    swaps: List[Swap] = []
    transfers: List[Transfer] = []

    for event in ordered_events:
        if not isinstance(event, DecodedEvent):
            continue

        elif event.classification == Classification.transfer:
            transfer = get_transfer(event)
            if transfer is not None:
                transfers.append(transfer)

        elif event.classification == Classification.swap:
            swap = _parse_swap(
                event,
                transfers
            )

            if swap is not None:
                swaps.append(swap)

    return swaps


def _parse_swap(
    event: DecodedEvent,
    transfers: List[Transfer]
) -> Optional[Swap]:

    classifier = get_classifier(event)
    if classifier is not None and issubclass(classifier, SwapClassifier):
        return classifier.parse_swap(event, transfers)
    return None
