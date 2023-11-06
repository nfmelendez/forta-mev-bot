from typing import List, Optional
from itertools import groupby


try:
    from src.classifiers.specs import get_classifier
    from src.schemas.classifiers import LiquidationClassifier
    from src.schemas.liquidations import Liquidation
    from src.schemas.events import Classification, ClassifiedEvent, DecodedEvent
except ModuleNotFoundError:
    from classifiers.specs import get_classifier
    from schemas.classifiers import LiquidationClassifier
    from schemas.liquidations import Liquidation
    from schemas.events import Classification, ClassifiedEvent, DecodedEvent

def has_liquidations(classified_events: List[ClassifiedEvent]) -> bool:
    liquidations_exist = False
    for classified_event in classified_events:
        if classified_event.classification == Classification.liquidate:
            liquidations_exist = True
    return liquidations_exist


def get_liquidations(classified_events: List[ClassifiedEvent]) -> List[Liquidation]:

    liquidations: List[Liquidation] = []

    get_transaction_hash = lambda e: e.transaction_hash

    events_by_transaction = groupby(
        sorted(classified_events, key=get_transaction_hash),
        key=get_transaction_hash,
    )

    for _, events in events_by_transaction:
        liquidations += _get_liquidations(
        list(events),
    )

    return liquidations


def _get_liquidations(classified_events: List[ClassifiedEvent]) -> List[Liquidation]:
    liquidations: List[Liquidation] = []
    liquidation_events: List[ClassifiedEvent] = []
    transfer_events: List[ClassifiedEvent] = []
    for event in classified_events:

        if not isinstance(event, DecodedEvent):
            continue

        if event.error == "Reverted":
            continue

        if event.classification == Classification.liquidate:
            liquidation_events.append(event)
        if event.classification == Classification.transfer:
            transfer_events.append(event)


    for le in liquidation_events:
        liquidation = _parse_liquidation(le, transfer_events)
        if liquidation is not None:
            liquidations.append(liquidation)

    return liquidations

def _parse_liquidation(
    event: DecodedEvent,
    transfer_events: List[ClassifiedEvent]
) -> Optional[Liquidation]:

    classifier = get_classifier(event)

    if classifier is not None and issubclass(classifier, LiquidationClassifier):
        return classifier.parse_liquidation(event, transfer_events)
    return None


