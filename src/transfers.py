from typing import Dict, List, Optional, Sequence



try:
    from src.classifiers.specs import get_classifier
    from src.schemas.classifiers import TransferClassifier
    from src.schemas.prices import ETH_TOKEN_ADDRESS
    from src.schemas.events import DecodedEvent
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from classifiers.specs import get_classifier
    from schemas.classifiers import TransferClassifier
    from schemas.prices import ETH_TOKEN_ADDRESS
    from schemas.events import DecodedEvent
    from schemas.transfers import Transfer

def get_transfers(events: List[DecodedEvent]) -> List[Transfer]:
    transfers = []

    for event in events:
        transfer = get_transfer(event)
        if transfer is not None:
            transfers.append(transfer)

    return transfers


def get_eth_transfers(events: List[DecodedEvent]) -> List[Transfer]:
    transfers = get_transfers(events)

    return [
        transfer
        for transfer in transfers
        if transfer.token_address == ETH_TOKEN_ADDRESS
    ]


def get_transfer(event: DecodedEvent) -> Optional[Transfer]:
    if isinstance(event, DecodedEvent):
        return _build_erc20_transfer(event)

    return None



def _build_erc20_transfer(event: DecodedEvent) -> Optional[Transfer]:
    classifier = get_classifier(event)
    if classifier is not None and issubclass(classifier, TransferClassifier):
        return classifier.get_transfer(event)

    return None


def filter_transfers(
    transfers: Sequence[Transfer],
    to_address: Optional[str] = None,
    from_address: Optional[str] = None,
) -> List[Transfer]:
    filtered_transfers = []

    for transfer in transfers:
        if to_address is not None and transfer.to_address != to_address:
            continue

        if from_address is not None and transfer.from_address != from_address:
            continue

        filtered_transfers.append(transfer)

    return filtered_transfers

