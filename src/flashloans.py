from typing import List, Optional


try:
    from src.classifiers.specs import get_classifier
    from src.schemas.events import Classification, ClassifiedEvent, DecodedEvent
    from src.schemas.transfers import Transfer
    from src.schemas.flashloan import FlashLoan
    from src.events import get_events_by_transaction_hash
    from src.schemas.classifiers import FlashLoanClassifier
except ModuleNotFoundError:
    from schemas.flashloan import FlashLoan
    from classifiers.specs import get_classifier
    from schemas.classifiers import FlashLoanClassifier
    from schemas.events import Classification, ClassifiedEvent, DecodedEvent
    from schemas.transfers import Transfer
    from events import get_events_by_transaction_hash


def get_flashloans(events: List[ClassifiedEvent]) -> List[FlashLoan]:
    flashloans = []

    for _, transaction_events in get_events_by_transaction_hash(events).items():
        flashloans += _get_flashloan_for_transaction(list(transaction_events))

    return flashloans


def _get_flashloan_for_transaction(events: List[ClassifiedEvent]) -> List[FlashLoan]:
    ordered_events = list(sorted(events, key=lambda t: t.log_index))

    flashloans: List[FlashLoan] = []
    transfers: List[Transfer] = []

    for event in ordered_events:
        if not isinstance(event, DecodedEvent):
            continue

        elif event.classification == Classification.flashloan:
            f = _parse_flashloan(
                event
            )

            if f is not None:
                flashloans.append(f)

    return flashloans


def _parse_flashloan(
    event: DecodedEvent,
) -> Optional[FlashLoan]:

    classifier = get_classifier(event)
    if classifier is not None and issubclass(classifier, FlashLoanClassifier):
        return classifier.parse_flashloan(event)
    return None
